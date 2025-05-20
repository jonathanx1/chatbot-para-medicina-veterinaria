from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify, make_response
import pymysql
import csv
import os
from io import StringIO
from flask_caching import Cache
from nlp_utils import extraer_sintomas_nlp, actualizar_diccionario_sinonimos
from modelo_diagnostico import predecir_diagnostico
from weasyprint import HTML
import time
from train_model import actualizar_modelo
from cargar_sintomas import cargar_diccionario_sinonimos
from typing import List, Tuple
import logging
from pymysql.err import MySQLError

logger = logging.getLogger(__name__)


app = Flask(__name__)
app.secret_key = 'key_1234'  # Cambia esta clave en producción

# Configuración de caché (tipo simple, en memoria)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['APP_START_TIME'] = time.time()
SINONIMO_A_SINTOMA = cargar_diccionario_sinonimos()

# ---------------------------
# Funciones de Base de Datos
# ---------------------------
def get_db_connection():
    """
    Establece una conexión a la base de datos leyendo las credenciales
    de las variables de entorno, con valores por defecto para desarrollo
    local.
    """
    try:
        conn = pymysql.connect(
            host=os.environ.get("DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            db=os.environ.get("DB_NAME", "chatbot_veterinario"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
            connect_timeout=5
        )
        logger.info("Conectado a MySQL %s:%s/%s",
                    os.environ.get("DB_HOST"), os.environ.get("DB_PORT"), os.environ.get("DB_NAME"))
        return conn
    except MySQLError as e:
        logger.error("No pude conectar a MySQL: %s", e)
        # opcionalmente relanza para que el error empiece a subir
        raise

# ---------------------------
# Funciones de Usuario y Autenticación
# ---------------------------
def authenticate_user(email: str, password: str):
    """
    Autentica un usuario buscando por email desencriptado
    y comparando la contraseña (texto plano) con la almacenada.
    """
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        sql = """
            SELECT
              id,
              AES_DECRYPT(password, 'mi_clave_secreta') AS pwd_bytes,
              AES_DECRYPT(nombre,   'mi_clave_secreta') AS nombre_bytes,
              AES_DECRYPT(rol,      'mi_clave_secreta') AS rol_bytes
            FROM usuarios
            WHERE AES_DECRYPT(email, 'mi_clave_secreta') = %s
            LIMIT 1
        """
        cur.execute(sql, (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            print(f"[DEBUG] authenticate_user: email no encontrado: {email!r}")
            return None

        user_id, pwd_bytes, name_bytes, role_bytes = row

        # Decodificar bytes a str (si existe)
        db_pwd   = pwd_bytes.decode('utf8')   if pwd_bytes   else None
        db_name  = name_bytes.decode('utf8')  if name_bytes  else None
        db_role  = role_bytes.decode('utf8')  if role_bytes  else None

        print(f"[DEBUG] authenticate_user: encontrado usuario id={user_id}, nombre={db_name!r}, rol={db_role!r}")

        # Comparar la contraseña tal cual (si no está usando hash)
        if db_pwd is not None and db_pwd == password:
            print(f"[DEBUG] authenticate_user: contraseña correcta para {email!r}")
            return user_id, db_name, db_role
        else:
            print(f"[DEBUG] authenticate_user: contraseña incorrecta para {email!r}")
            return None

    except Exception as e:
        print("Error en authenticate_user:", e)
        return None


# ---------------------------
# Funciones del Chatbot y Diagnóstico
# ---------------------------
def buscar_enfermedades(sintomas_usuario: str, especie: str) -> List[Tuple]:
    """
    Busca enfermedades que coincidan con los síntomas y que pertenezcan
    a la especie indicada ('perro' -> especie_id=1, 'gato' -> 2),
    ordenadas por número de síntomas coincidentes (match_count).
    """
    especie_map = {'perro': 1, 'gato': 2}
    especie_id = especie_map.get(especie.lower())
    if especie_id is None:
        print(f"Especie '{especie}' no soportada.")
        return []

    sintomas = [s.strip().lower() for s in sintomas_usuario.split(',') if s.strip()]
    if not sintomas:
        print("No se proporcionaron síntomas para buscar.")
        return []

    like_clauses = []
    count_expressions = []
    params = []

    for sint in sintomas:
        like_clauses.append("LOWER(sintomas) LIKE %s")
        count_expressions.append("(LOWER(sintomas) LIKE %s)")
        params.append(f"%{sint}%")
        params.append(f"%{sint}%")  # Para el conteo y para la cláusula WHERE

    where_sql = " OR ".join(like_clauses)
    count_sql = " + ".join(count_expressions)

    sql = f"""
        SELECT 
          id, 
          nombre, 
          sintomas, 
          tratamiento, 
          prevencion,
          ({count_sql}) AS match_count
        FROM enfermedades
        WHERE especie_id = %s
          AND ({where_sql})
        ORDER BY match_count DESC, nombre
        LIMIT 10
    """

    exec_params = [especie_id] + params

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(sql, tuple(exec_params))
            resultados = cur.fetchall()
    except Exception as e:
        print("Error en buscar_enfermedades:", e)
        resultados = []
    finally:
        conn.close()

    if not resultados:
        print("No se encontraron enfermedades que coincidan con los síntomas proporcionados.")
    return resultados


def procesar_consulta_usuario(texto_usuario: str, especie_id: int):
    """
    Procesa la consulta completa (texto_usuario) para la especie dada.
    Devuelve:
      - resultados_db: lista de tuplas (id, nombre, síntomas, tratamiento, prevención)
      - sint_afirm: lista de síntomas afirmados
      - diagnostico_ml: cadena con diagnóstico ML o None
      - mensaje_error: cadena con mensaje de error o None
    """
    try:
        # 1) Extraer síntomas afirmados/negados
        sint_afirm, sint_neg = extraer_sintomas_nlp(texto_usuario)
        print("=== Síntomas extraídos (REGEX) ===", sint_afirm, sint_neg)

        if not sint_afirm:
            mensaje_error = "No se detectaron síntomas conocidos en la descripción. Por favor, describe con más detalles o usa otros síntomas."
            return [], [], None, mensaje_error

        # 2) Convertir la lista de síntomas afirmados a un string
        sintomas_string = ", ".join(sint_afirm)
        print(f"=== Síntomas para búsqueda: {sintomas_string} --- especie_id: {especie_id}")

        # 3) Buscar enfermedades en BD con el especie_id
        resultados_db = buscar_enfermedades(sintomas_string, especie_id)
        print(f"=== Resultados encontrados en BD: {len(resultados_db)}")

        if not resultados_db:
            mensaje_error = "No se encontraron enfermedades que coincidan con los síntomas proporcionados."
            return [], sint_afirm, None, mensaje_error

        # 4) Predicción del modelo de ML (también recibe especie_id si tu modelo lo necesita)
        pred = predecir_diagnostico(sint_afirm, especie_id)
        print(f"=== Resultado de predicción ML: {pred}")

        # 5) Convertir la clase ML a nombre legible
        diagnosticos = obtener_diccionario_diagnosticos()
        diagnostico_ml = diagnosticos.get(pred, "Desconocido")
        print("=== Diagnóstico ML legible ===", diagnostico_ml)

        return resultados_db, sint_afirm, diagnostico_ml, None

    except Exception as e:
        print(f"Error en procesar_consulta_usuario: {e}")
        return [], [], None, "Error interno al procesar la consulta."



@cache.memoize(timeout=60)
def procesar_consulta_usuario_cached(texto_usuario):
    return procesar_consulta_usuario(texto_usuario)
def obtener_diccionario_diagnosticos():
    """
    Devuelve un diccionario que mapea el nombre interno de la enfermedad
    (lo que retorna el modelo ML) al nombre legible.
    Asumimos que el ML devuelve directamente el campo 'nombre' de la tabla.
    """
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        # 1) Ejecutar la consulta para obtener todos los nombres
        cursor.execute("SELECT nombre FROM enfermedades")
        # 2) Leer los resultados
        rows = cursor.fetchall()  # cada fila es (nombre,)
        cursor.close()
        conn.close()
        # 3) Construir el diccionario {nombre: nombre}
        return {row[0]: row[0] for row in rows if row[0] is not None}
    except Exception as e:
        print("Error en obtener_diccionario_diagnosticos:", e)
        return {}


def buscar_consultas_relacionadas(sintomas_list, consulta_actual):
    if not sintomas_list:
        return []
    try:
        connection = get_db_connection()
        # Uso de un "context manager" para el cursor (si la librería lo permite)
        with connection.cursor() as cursor:
            condiciones = " OR ".join(["consulta LIKE %s" for _ in sintomas_list])
            sql = f"SELECT DISTINCT consulta FROM consultas WHERE {condiciones} AND consulta != %s ORDER BY fecha DESC LIMIT 5"
            params = [f"%{s}%" for s in sintomas_list] + [consulta_actual]
            cursor.execute(sql, params)
            related = cursor.fetchall()
        connection.close()
        return [r[0] for r in related]
    except Exception as e:
        print("Error al buscar consultas relacionadas:", e)
        return []


def registrar_consulta(usuario_id, consulta, respuesta):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO consultas (usuario_id, consulta, respuesta) VALUES (%s, %s, %s)"
        cursor.execute(sql, (usuario_id, consulta, respuesta))
        connection.commit()
        cursor.close()
        connection.close()
        print("Consulta registrada en la base de datos.")
    except Exception as e:
        print("Error al registrar la consulta:", e)

def registrar_feedback(usuario_id, comentario, rating):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "INSERT INTO feedback (usuario_id, comentario, rating) VALUES (%s, %s, %s)"
        cursor.execute(sql, (usuario_id, comentario, rating))
        connection.commit()
        cursor.close()
        connection.close()
        print("Feedback registrado en la base de datos.")
    except Exception as e:
        print("Error al registrar el feedback:", e)

# ---------------------------
# Rutas de la Aplicación
# ---------------------------

# Login y Logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = authenticate_user(email, password)
        if user:
            user_id, user_name, user_role = user
            session['user_id'] = user_id
            session['user_name'] = user_name
            session['user_role'] = user_role
            session['user_email'] = email
            flash("Inicio de sesión exitoso.")
            # Redirige según el rol:
            if user_role.lower() == 'profesor':
                return redirect(url_for('reportes'))
            elif user_role.lower() == 'administrativo':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('index'))
        else:
            flash("Credenciales incorrectas.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión.")
    return redirect(url_for('login'))

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para continuar.", "warning")
        return redirect(url_for('login'))

    error_current = False

    if request.method == 'POST':
        actual   = request.form.get('current_password')
        nueva    = request.form.get('new_password')
        confirma = request.form.get('confirm_password')

        # Campos vacíos
        if not actual or not nueva or not confirma:
            flash("Completa todos los campos de contraseña.", "danger")
            return redirect(url_for('perfil'))

        # Nuevas no coinciden
        if nueva != confirma:
            flash("La nueva contraseña y su confirmación no coinciden.", "danger")
            return redirect(url_for('perfil'))

        # Obtener la contraseña actual de la BD
        try:
            conn = get_db_connection()
            cur  = conn.cursor()
            cur.execute("""
                SELECT CAST(AES_DECRYPT(password, 'mi_clave_secreta') AS CHAR)
                FROM usuarios
                WHERE id = %s
            """, (session['user_id'],))
            fila = cur.fetchone()
            cur.close()
            conn.close()
        except Exception as e:
            print("Error al consultar contraseña actual:", e)
            flash("Ocurrió un error interno.", "danger")
            return redirect(url_for('perfil'))

        # Si no coincide, render con error inline
        if not fila or fila[0] != actual:
            error_current = True
        else:
            # Actualizamos la contraseña
            try:
                conn = get_db_connection()
                cur  = conn.cursor()
                cur.execute("""
                    UPDATE usuarios
                    SET password = AES_ENCRYPT(%s, 'mi_clave_secreta')
                    WHERE id = %s
                """, (nueva, session['user_id']))
                conn.commit()
                cur.close()
                conn.close()
                flash("Contraseña actualizada correctamente.", "success")
                return redirect(url_for('perfil'))
            except Exception as e:
                print("Error al actualizar la contraseña:", e)
                flash("Error al actualizar la contraseña.", "danger")
                return redirect(url_for('perfil'))

    # Al llegar aquí, o en GET, renderizamos mostrando error_current si aplica
    template = 'perfil_admin.html' if session.get('user_role','').lower()=='administrativo' else 'perfil.html'
    return render_template(
        template,
        user_name   = session['user_name'],
        user_email  = session['user_email'],
        user_role   = session['user_role'],
        error_current=error_current
    )


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para dejar feedback.")
        return redirect(url_for('login'))
    if request.method == 'POST':
        comentario = request.form.get('comentario')
        rating = request.form.get('rating')
        if not comentario or not rating:
            flash("Por favor, completa todos los campos.")
            return redirect(url_for('feedback'))
        try:
            registrar_feedback(session['user_id'], comentario, int(rating))
            flash("Gracias por tu feedback.")
            return redirect(url_for('index'))
        except Exception as e:
            flash("Error al registrar el feedback.")
            return redirect(url_for('feedback'))
    return render_template('feedback.html', user_name=session.get('user_name'))

# Página principal para usuarios normales (Chatbot)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para continuar.")
        return redirect(url_for('login'))
    results = None
    consulta = None
    related_queries = []
    diagnostico_ml = None
    if request.method == 'POST':
        consulta = request.form.get('consulta')
        if consulta:
            results, sintomas, diagnostico_ml = procesar_consulta_usuario(consulta)

            # Solo registra la consulta si se encontraron resultados
            if results:
                registrar_consulta(session['user_id'], consulta, "Consulta procesada")
            else:
                flash("No se encontraron coincidencias. La consulta no se registrará.")
            if sintomas:
                related_queries = buscar_consultas_relacionadas(sintomas, consulta)
        else:
            flash("Por favor ingresa una consulta.")
            return redirect(url_for('index'))
    return render_template('index.html', user_name=session.get('user_name'),
                           results=results, consulta=consulta, related_queries=related_queries,
                           diagnostico_ml=diagnostico_ml)

# Página de inicio para administradores (Chatbot + enlace al panel)
@app.route('/admin/home', methods=['GET', 'POST'])
def admin_home():
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado.")
        return redirect(url_for('login'))
    results = None
    consulta = None
    related_queries = []
    diagnostico_ml = None
    if request.method == 'POST':
        consulta = request.form.get('consulta')
        if consulta:
            results, sintomas, diagnostico_ml = procesar_consulta_usuario_cached(consulta)
            if results:
                registrar_consulta(session['user_id'], consulta, "Consulta procesada")
            else:
                flash("No se encontraron coincidencias. La consulta no se registrará.")
            if sintomas:
                related_queries = buscar_consultas_relacionadas(sintomas, consulta)
        else:
            flash("Por favor ingresa una consulta.")
            return redirect(url_for('admin_home'))
    return render_template('admin_home.html', user_name=session.get('user_name'),
                           results=results, consulta=consulta, related_queries=related_queries,
                           diagnostico_ml=diagnostico_ml)

@app.route('/profesor/reportes', methods=['GET', 'POST'])
def reportes():
    if 'user_id' not in session or session.get('user_role').lower() != 'profesor':
        flash("Acceso denegado. Esta área es exclusiva para profesores.")
        return redirect(url_for('index'))
    start_date = request.form.get('start_date') if request.method == 'POST' else None
    end_date = request.form.get('end_date') if request.method == 'POST' else None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # Obtener total de consultas
        if start_date and end_date:
            sql_total = "SELECT COUNT(*) FROM consultas WHERE fecha BETWEEN %s AND %s"
            cursor.execute(sql_total, (start_date, end_date))
        else:
            sql_total = "SELECT COUNT(*) FROM consultas"
            cursor.execute(sql_total)
        total_consultas = cursor.fetchone()[0]
        
        # Consulta para agrupar las consultas por fecha
        if start_date and end_date:
            sql_group = """
                SELECT DATE(fecha) as fecha, COUNT(*) as total
                FROM consultas
                WHERE fecha BETWEEN %s AND %s
                GROUP BY DATE(fecha)
                ORDER BY DATE(fecha)
            """
            cursor.execute(sql_group, (start_date, end_date))
        else:
            sql_group = """
                SELECT DATE(fecha) as fecha, COUNT(*) as total
                FROM consultas
                GROUP BY DATE(fecha)
                ORDER BY DATE(fecha)
            """
            cursor.execute(sql_group)
        
        rows = cursor.fetchall()
        # Convertir las fechas a string en formato YYYY-MM-DD
        fechas = [row[0].strftime("%Y-%m-%d") if hasattr(row[0], 'strftime') else row[0] for row in rows]
        consultas_diarias = [row[1] for row in rows]
        
        cursor.close()
        connection.close()

        data = {
            'total_consultas': total_consultas,
            'start_date': start_date,
            'end_date': end_date,
            'fechas': fechas,
            'consultas_diarias': consultas_diarias
        }
        print("Fechas:", data.get('fechas'))
        print("Consultas Diarias:", data.get('consultas_diarias'))
        return render_template('profesor_reportes.html', data=data, user_name=session.get('user_name'))
    except Exception as e:
        print("Error al generar reportes:", e)
        flash("Error al generar los reportes.")
        return redirect(url_for('index'))


# Detalle de una enfermedad
@app.route('/detalle/<int:enfermedad_id>')
def detalle(enfermedad_id):
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para continuar.")
        return redirect(url_for('login'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT id, nombre, sintomas, tratamiento, prevencion FROM enfermedades WHERE id = %s"
        cursor.execute(sql, (enfermedad_id,))
        det = cursor.fetchone()
        cursor.close()
        connection.close()
        if det:
            return render_template('detalle.html', detalle=det, user_name=session.get('user_name'))
        else:
            flash("Enfermedad no encontrada.")
            return redirect(url_for('index'))
    except Exception as e:
        print("Error en detalle:", e)
        flash("Error al cargar el detalle de la enfermedad.")
        return redirect(url_for('index'))

@app.route('/historial', methods=['GET', 'POST'])
def historial():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para ver el historial.")
        return redirect(url_for('login'))

    filtros = {
        "start_date": "",
        "end_date": "",
        "keyword": "",
        "diagnosis": ""
    }

    # 1) Base de la consulta con WHERE 1=1
    if session.get('user_role', '').lower() == 'administrativo':
        sql = """
            SELECT id, consulta, respuesta, fecha, usuario_id 
            FROM consultas
            WHERE 1=1
        """
        params = []
    else:
        sql = """
            SELECT id, consulta, respuesta, fecha 
            FROM consultas
            WHERE usuario_id = %s
        """
        params = [session['user_id']]

    # 2) Si viene POST, leer filtros y concatenar AND ...
    if request.method == 'POST':
        filtros["start_date"] = request.form.get('start_date', '')
        filtros["end_date"]   = request.form.get('end_date', '')
        filtros["keyword"]    = request.form.get('keyword', '')
        filtros["diagnosis"]  = request.form.get('diagnosis', '')

        if filtros["start_date"]:
            sql += " AND fecha >= %s"
            params.append(filtros["start_date"])
        if filtros["end_date"]:
            sql += " AND fecha <= %s"
            params.append(filtros["end_date"])
        if filtros["keyword"]:
            sql += " AND consulta LIKE %s"
            params.append(f"%{filtros['keyword']}%")
        if filtros["diagnosis"]:
            sql += " AND respuesta LIKE %s"
            params.append(f"%{filtros['diagnosis']}%")

    # 3) Ordenar siempre al final
    sql += " ORDER BY fecha DESC"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(sql, tuple(params))
        registros = cursor.fetchall()
    except Exception as e:
        print("Error al obtener el historial:", e)
        flash("Error al cargar el historial.")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        connection.close()

    # 4) Elegir plantilla según rol
    plantilla = 'historial_admin.html' if session.get('user_role','').lower()=='administrativo' else 'historial.html'
    return render_template(plantilla,
                           historial=registros,
                           user_name=session.get('user_name'),
                           filtros=filtros)
STOPWORDS = {
    'mi','tiene','tengo','tuvo','tu', 'pero','y','con','de','en',
    'el','la','los','las','un','una','unos','unas','pequeño','grande',
    'perro','gato', 'mas', 'ninguno'
}
def detectar_sintomas_no_reconocidos(
    texto_usuario: str,
    sintomas_extraidos: List[str]
) -> List[str]:
    """
    Devuelve las palabras del texto_usuario que:
     - No forman parte de ningún síntoma_extraido.
     - No están en STOPWORDS.
     - Tienen longitud > 2 y son alfabéticas.
    """
    tokens = set(texto_usuario.lower().split())
    partes_sintomas = {tok for s in sintomas_extraidos for tok in s.split()}
    candidatos = [
        w for w in tokens
        if w not in partes_sintomas
        and w not in STOPWORDS
        and w.isalpha()
        and len(w) > 2
    ]
    return candidatos

@app.route('/api/consulta', methods=['POST'])
def api_consulta():
    # --- 1) Validación inicial ---
    if not request.form:
        return jsonify({'error': 'No se recibió ningún dato de formulario.'}), 400

    consulta = request.form['consulta'].strip().lower()
    especie = request.form['especie'].lower()

    especie_map = {'perro': 1, 'gato': 2}
    if especie not in especie_map:
        return jsonify({'error': f"Especie '{especie}' no soportada."}), 400

    # --- 1.1) Verificación de coherencia especie-consulta ---
    if ('gato' in consulta and especie != 'gato') or ('perro' in consulta and especie != 'perro'):
        return jsonify({
            'consulta': consulta,
            'sintomas_detectados': [],
            'diagnostico_sugerido': None,
            'resultados': [],
            'related_queries': [],
            'mensaje_extra': (
                f"Detectamos que estás hablando de un {'gato' if 'gato' in consulta else 'perro'}, "
                f"pero seleccionaste '{especie}' como especie. Por favor, corrige la especie seleccionada."
            ),
            'follow_up': None
        }), 200

    especie_id = especie_map[especie]

    # --- 2) Extraer síntomas afirmados y negados ---
    sint_afirm, sint_neg = extraer_sintomas_nlp(consulta)

    # --- 3) Validar términos no reconocidos ---
    no_reconocidos = detectar_sintomas_no_reconocidos(consulta, sint_afirm + sint_neg)
    if no_reconocidos:
        return jsonify({
            'consulta': consulta,
            'sintomas_detectados': [],
            'diagnostico_sugerido': None,
            'resultados': [],
            'related_queries': [],
            'mensaje_extra': (
                "No se reconocieron estos términos como síntomas válidos: "
                f"{', '.join(no_reconocidos)}. Por favor usa síntomas conocidos."
            ),
            'follow_up': None
        }), 200

    # --- 4) Si no hay síntomas afirmados válidos ---
    if not sint_afirm:
        return jsonify({
            'consulta': consulta,
            'sintomas_detectados': [],
            'diagnostico_sugerido': None,
            'resultados': [],
            'related_queries': [],
            'mensaje_extra': (
                "No se detectaron síntomas. Por favor describe con más detalle "
                "o utiliza otros términos reconocidos."
            ),
            'follow_up': None
        }), 200

    # --- 5) Procesamiento completo (BD + ML) ---
    resultados, sint_afirm, diagnostico_ml, mensaje_error = procesar_consulta_usuario(
        consulta, especie_id
    )

    # --- 6) Manejo de error desde el procesamiento ---
    if mensaje_error:
        return jsonify({
            'consulta': consulta,
            'sintomas_detectados': sint_afirm,
            'diagnostico_sugerido': None,
            'resultados': [],
            'related_queries': [],
            'mensaje_extra': mensaje_error,
            'follow_up': None
        }), 200

    # --- 7) Determinar sugerido y registrar ---
    sugerido = resultados[0][1] if resultados else diagnostico_ml
    if sugerido and session.get('user_id'):
        registrar_consulta(session['user_id'], consulta, sugerido)

    # --- 8) Devolver respuesta exitosa ---
    return jsonify({
        'consulta': consulta,
        'sintomas_detectados': sint_afirm,
        'diagnostico_sugerido': sugerido,
        'resultados': [
            {
                'id': r[0],
                'nombre': r[1],
                'sintomas': r[2],
                'tratamiento': r[3],
                'prevencion': r[4]
            } for r in resultados
        ],
        'related_queries': buscar_consultas_relacionadas(sint_afirm, consulta),
        'mensaje_extra': "",
        'follow_up': None
    }), 200



def buscar_enfermedades(sintomas_usuario: str, especie_id: int):
    """
    Busca en la tabla 'enfermedades' sólo las que pertenezcan a la especie indicada
    y cuyo campo 'sintomas' contenga alguno de los síntomas dados.
    """
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        sintomas = [s.strip().lower() for s in sintomas_usuario.split(',') if s.strip()]
        if not sintomas:
            return []
        placeholders = " OR ".join(["LOWER(sintomas) LIKE %s"] * len(sintomas))
        sql = (
            "SELECT id, nombre, sintomas, tratamiento, prevencion "
            "FROM enfermedades "
            "WHERE especie_id = %s AND (" + placeholders + ")"
        )
        params = [especie_id] + [f"%{s}%" for s in sintomas]
        cur.execute(sql, params)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados
    except Exception as e:
        print("Error en buscar_enfermedades:", e)
        return []


# -------------------
# Función buscar_enfermedades actualizada:
def buscar_enfermedades(sintomas_usuario: str, especie_id: int):
    """
    Busca enfermedades que pertenezcan a la especie dada y ordena por coincidencia
    entre síntomas del usuario y síntomas de la enfermedad.
    
    Devuelve lista ordenada (mayor coincidencia primero) de:
    (id, nombre, sintomas, tratamiento, prevencion)
    """
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, nombre, sintomas, tratamiento, prevencion "
                    "FROM enfermedades WHERE especie_id = %s",
                    (especie_id,)
                )
                enfermedades = cursor.fetchall()
    except Exception as e:
        print("Error en buscar_enfermedades:", e)
        return []

    # Procesar síntomas del usuario a conjunto único y en minúsculas
    sintomas_usuario_set = set(s.strip().lower() for s in sintomas_usuario.split(',') if s.strip())

    if not sintomas_usuario_set:
        return []

    def calcular_puntaje(enfermedad):
        _, _, sintomas_csv, _, _ = enfermedad
        sintomas_enf_set = set(s.strip().lower() for s in sintomas_csv.split(',') if s.strip())
        coincidencias = sintomas_usuario_set.intersection(sintomas_enf_set)
        penalizacion = len(sintomas_usuario_set - sintomas_enf_set)
        return len(coincidencias) - penalizacion  # Balancea coincidencias vs faltantes

    # Ordenar enfermedades por puntaje descendente
    enfermedades_ordenadas = sorted(
        enfermedades,
        key=calcular_puntaje,
        reverse=True
    )

    return enfermedades_ordenadas



@app.route('/exportar', methods=['GET'])
def exportar_form():
    filtros = {
        'start_date': request.args.get('start_date', ''),
        'end_date': request.args.get('end_date', ''),
        'keyword': request.args.get('keyword', ''),
        'diagnosis': request.args.get('diagnosis', ''),
        'formato': request.args.get('formato', ''),
    }
    return render_template('exportar.html', filtros=filtros)



@app.route('/exportar', methods=['GET', 'POST'])
def exportar():
    if 'user_id' not in session:
        flash("Por favor, inicia sesión para exportar tu historial.", "warning")
        return redirect(url_for('login'))
    
    # Leer los filtros
    start = request.values.get('start_date', '').strip()
    end   = request.values.get('end_date', '').strip()
    key   = request.values.get('keyword', '').strip()
    diag  = request.values.get('diagnosis', '').strip()
    formato = request.values.get('formato', '').lower()

    filtros = {
        'start_date': start,
        'end_date':   end,
        'keyword':    key,
        'diagnosis':  diag
    }

    if request.method == 'GET' and not formato:
        return render_template('exportar.html', filtros=filtros)

    # Construir SQL con filtros
    sql = "SELECT fecha, consulta, respuesta FROM consultas WHERE usuario_id = %s"
    params = [session['user_id']]
    if start:
        sql += " AND fecha >= %s"
        params.append(start)
    if end:
        sql += " AND fecha <= %s"
        params.append(end)
    if key:
        sql += " AND consulta LIKE %s"
        params.append(f"%{key}%")
    if diag:
        sql += " AND respuesta LIKE %s"
        params.append(f"%{diag}%")
    sql += " ORDER BY fecha DESC"

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(sql, tuple(params))
        registros = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    if formato == 'csv':
        

        si = StringIO()
        writer = csv.writer(si, delimiter=';', quoting=csv.QUOTE_ALL)
        bom = u'\ufeff'
        writer.writerow(["Fecha", "Consulta", "Diagnóstico"])

        for fecha, consulta, respuesta in registros:
            fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S") if hasattr(fecha, 'strftime') else fecha
            consulta_limpia = str(consulta).replace('\n', ' ').replace('\r', ' ').strip()
            respuesta_limpia = str(respuesta).replace('\n', ' ').replace('\r', ' ').strip()
            writer.writerow([fecha_str, consulta_limpia, respuesta_limpia])

        data = bom + si.getvalue()
        si.close()
        return Response(
            data,
            mimetype="text/csv; charset=utf-8",
            headers={"Content-Disposition": "attachment;filename=historial.csv"}
        )

    elif formato == 'pdf':
        from weasyprint import HTML
        html = render_template('historial_pdf.html', registros=registros, user_name=session.get('user_name'))
        pdf = HTML(string=html).write_pdf()
        return Response(
            pdf,
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment;filename=historial.pdf"}
        )

    else:
        flash("Formato no soportado.", "danger")
        return redirect(url_for('historial'))



# Panel administrativo (se abre en otra página)
@app.route('/admin/panel')
def admin_panel():
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.")
        return redirect(url_for('index'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM consultas")
        total_consultas = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        total_usuarios = cursor.fetchone()[0]
        cursor.execute("SELECT DATE(fecha) as fecha, COUNT(*) as total FROM consultas GROUP BY DATE(fecha) ORDER BY DATE(fecha)")
        stats = cursor.fetchall()
        cursor.execute("SELECT AVG(rating) FROM feedback")
        avg_rating = cursor.fetchone()[0]
        cursor.execute("SELECT rating, COUNT(*) FROM feedback GROUP BY rating ORDER BY rating")
        feedback_stats = cursor.fetchall()
        cursor.close()
        connection.close()
        labels = [str(row[0]) for row in stats]
        data = [row[1] for row in stats]
        feedback_labels = [str(row[0]) for row in feedback_stats]
        feedback_data = [row[1] for row in feedback_stats]
        return render_template('admin.html',
                               total_consultas=total_consultas,
                               total_usuarios=total_usuarios,
                               avg_rating=avg_rating,
                               feedback_labels=feedback_labels,
                               feedback_data=feedback_data,
                               labels=labels,
                               data=data,
                               user_name=session.get('user_name'))
    except Exception as e:
        print("Error en el panel de administración:", e)
        flash("Error al cargar el panel de administración.")
        return redirect(url_for('index'))
    except Exception as e:
        print("Error en el panel de administración:", e)
        flash("Error al cargar el panel de administración.")
        return redirect(url_for('index'))

# Ver feedback (solo para admins)
@app.route('/ver-feedback')
def ver_feedback():
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.")
        return redirect(url_for('index'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT id, comentario, rating, fecha, usuario_id FROM feedback ORDER BY fecha DESC"
        cursor.execute(sql)
        feedbacks = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('ver_feedback.html', feedbacks=feedbacks, user_name=session.get('user_name'))
    except Exception as e:
        print("Error al obtener el feedback:", e)
        flash("Error al cargar el feedback.")
        return redirect(url_for('admin_panel'))

# FAQ
@app.route('/faq')
def faq():
    faqs = [
        {
            "question": "¿Qué debo hacer si mi mascota tiene fiebre?",
            "answer": "Asegúrate de que esté hidratada y consulta a un veterinario."
        },
        {
            "question": "¿Cuáles son los síntomas del parvovirus?",
            "answer": "Vómitos, diarrea y fiebre son comunes en parvovirus, sobre todo en cachorros."
        },
        {
            "question": "¿Cómo puedo prevenir enfermedades en mi mascota?",
            "answer": "Mantenla vacunada, con una dieta adecuada y visitas regulares al veterinario."
        },
        {
            "question": "¿El Chatbot Veterinario reemplaza al veterinario?",
            "answer": "No, ofrece diagnósticos preliminares; siempre se recomienda una consulta profesional."
        }
    ]
    return render_template('faq.html', faqs=faqs, user_name=session.get('user_name'))

@app.route('/acerca_de')
def acerca_de():
    if session.get('user_role') and session.get('user_role').lower() == 'administrativo':
        return render_template('acerca_de_admin.html', user_name=session.get('user_name'))
    else:
        return render_template('acerca_de.html', user_name=session.get('user_name'))


# Tendencias (solo para admins)
@app.route('/tendencias')
def tendencias():
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.")
        return redirect(url_for('index'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, nombre FROM enfermedades")
        diseases = cursor.fetchall()
        tendencias = []
        for disease in diseases:
            disease_id, disease_name = disease
            query = "SELECT COUNT(*) FROM consultas WHERE respuesta LIKE %s"
            param = f"%{disease_name}%"
            cursor.execute(query, (param,))
            count = cursor.fetchone()[0]
            tendencias.append((disease_name, count))
        cursor.close()
        connection.close()
        tendencias = sorted(tendencias, key=lambda x: x[1], reverse=True)
        return render_template('tendencias.html', tendencias=tendencias, user_name=session.get('user_name'))
    except Exception as e:
        print("Error al obtener tendencias:", e)
        flash("Error al cargar las tendencias.")
        return redirect(url_for('admin_panel'))

# Rutas CRUD para gestionar enfermedades (solo para admins)
@app.route('/admin/enfermedades')
def admin_enfermedades():
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.")
        return redirect(url_for('index'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT id, nombre, sintomas, tratamiento, prevencion FROM enfermedades ORDER BY nombre"
        cursor.execute(sql)
        enfermedades = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('admin_enfermedades.html', enfermedades=enfermedades, user_name=session.get('user_name'))
    except Exception as e:
        print("Error al obtener la lista de enfermedades:", e)
        flash("Error al cargar la lista de enfermedades.")
        return redirect(url_for('admin_panel'))

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)

@app.route('/admin/enfermedad/agregar', methods=['GET', 'POST'])
def agregar_enfermedad():
    # Solo administradores
    if 'user_id' not in session or session.get('user_role', '').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.", "warning")
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre     = request.form.get('nombre', '').strip()
        sintomas   = request.form.get('sintomas', '').strip()
        tratamiento= request.form.get('tratamiento', '').strip()
        prevencion = request.form.get('prevencion', '').strip()
        especie_id = request.form.get('especie_id')  # 1=Perro, 2=Gato

        # Validación básica
        if not (nombre and sintomas and tratamiento and prevencion and especie_id):
            flash("Por favor, completa todos los campos.", "danger")
            return redirect(url_for('agregar_enfermedad'))

        # Verificamos si ya existe una enfermedad con el mismo nombre
        try:
            conn = get_db_connection()
            cur  = conn.cursor()
            cur.execute("SELECT * FROM enfermedades WHERE nombre = %s", (nombre,))
            existente = cur.fetchone()

            if existente:
                cur.close()
                conn.close()
                error_nombre = "Ya existe una enfermedad con ese nombre."
                return render_template(
                    'agregar_enfermedad.html',
                    user_name=session.get('user_name'),
                    especies=[{'id': 1, 'nombre': 'Perro'}, {'id': 2, 'nombre': 'Gato'}],
                    error_nombre=error_nombre
                )

            # Si no existe, agregamos la enfermedad
            sql = """
                INSERT INTO enfermedades
                  (nombre, sintomas, tratamiento, prevencion, especie_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cur.execute(sql, (nombre, sintomas, tratamiento, prevencion, especie_id))
            conn.commit()
            cur.close()
            conn.close()

            # Reentrenar el modelo y recargar el diccionario de sinónimos para NLP
            actualizar_modelo()
            actualizar_diccionario_sinonimos()

            flash("Enfermedad agregada y sistema actualizado correctamente.", "success")
            return redirect(url_for('admin_enfermedades'))

        except Exception as e:
            app.logger.error(f"Error al agregar enfermedad: {e}")
            flash("Ocurrió un error al agregar la enfermedad.", "danger")
            return redirect(url_for('agregar_enfermedad'))

    # GET: mostrar formulario
    return render_template(
        'agregar_enfermedad.html',
        user_name=session.get('user_name'),
        especies=[{'id': 1, 'nombre': 'Perro'}, {'id': 2, 'nombre': 'Gato'}],
        error_nombre=None
    )

@app.route('/admin/enfermedad/editar/<int:enfermedad_id>', methods=['GET', 'POST'])
def editar_enfermedad(enfermedad_id):
    if 'user_id' not in session or session.get('user_role', '').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.", "danger")
        return redirect(url_for('index'))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Para acceder como diccionario

    if request.method == 'POST':
        nombre      = request.form.get('nombre', '').strip()
        sintomas    = request.form.get('sintomas', '').strip()
        tratamiento = request.form.get('tratamiento', '').strip()
        prevencion  = request.form.get('prevencion', '').strip()
        clase_ml    = request.form.get('clase_ml', '').strip()

        if not all([nombre, sintomas, tratamiento, prevencion]):
            flash("Por favor, completa todos los campos.", "danger")
            return render_template(
                'editar_enfermedad.html',
                enfermedad=request.form,
                user_name=session.get('user_name'),
                error_nombre=None
            )

        try:
            cursor.execute("""
                SELECT id FROM enfermedades 
                WHERE LOWER(nombre) = LOWER(%s) AND id != %s
            """, (nombre, enfermedad_id))
            existente = cursor.fetchone()

            if existente:
                # Mostrar error sin redirigir
                return render_template(
                    'editar_enfermedad.html',
                    enfermedad=request.form,
                    user_name=session.get('user_name'),
                    error_nombre="Ya existe otra enfermedad con ese nombre."
                )

            cursor.execute("""
                UPDATE enfermedades 
                SET nombre=%s, sintomas=%s, tratamiento=%s, prevencion=%s, clase_ml=%s 
                WHERE id=%s
            """, (nombre, sintomas, tratamiento, prevencion, clase_ml, enfermedad_id))
            connection.commit()

            actualizar_modelo()
            flash("Enfermedad actualizada y modelo reentrenado correctamente.", "success")
            return redirect(url_for('admin_enfermedades'))

        except Exception as e:
            print("Error al editar enfermedad:", e)
            flash("Error al actualizar la enfermedad.", "danger")
            return redirect(url_for('editar_enfermedad', enfermedad_id=enfermedad_id))

        finally:
            cursor.close()
            connection.close()

    else:
        try:
            cursor.execute("""
                SELECT id, nombre, sintomas, tratamiento, prevencion, clase_ml 
                FROM enfermedades WHERE id = %s
            """, (enfermedad_id,))
            enfermedad = cursor.fetchone()

            if enfermedad:
                return render_template(
                    'editar_enfermedad.html',
                    enfermedad=enfermedad,
                    user_name=session.get('user_name'),
                    error_nombre=None
                )
            else:
                flash("Enfermedad no encontrada.", "danger")
                return redirect(url_for('admin_enfermedades'))

        except Exception as e:
            print("Error al obtener enfermedad:", e)
            flash("Error al cargar la enfermedad.", "danger")
            return redirect(url_for('admin_enfermedades'))

        finally:
            cursor.close()
            connection.close()

@app.route('/admin/enfermedad/eliminar/<int:enfermedad_id>', methods=['POST'])
def eliminar_enfermedad(enfermedad_id):
    if 'user_id' not in session or session.get('user_role').lower() != 'administrativo':
        flash("Acceso denegado. Esta área es exclusiva para usuarios administrativos.")
        return redirect(url_for('index'))
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM enfermedades WHERE id = %s", (enfermedad_id,))
        connection.commit()
        cursor.close()
        connection.close()

        # Reentrenar el modelo tras eliminación
        actualizar_modelo()

        flash("Enfermedad eliminada y modelo actualizado correctamente.")
        return redirect(url_for('admin_enfermedades'))
    except Exception as e:
        print("Error al eliminar enfermedad:", e)
        flash("Error al eliminar la enfermedad.")
        return redirect(url_for('admin_enfermedades'))

from flask import request, render_template, make_response, flash, session, redirect, url_for
from weasyprint import HTML

@app.route('/profesor/reportes/pdf', methods=['GET'])
def reportes_pdf():
    if 'user_id' not in session or session.get('user_role','').lower() != 'profesor':
        flash("Acceso denegado. Área solo para profesores.", "warning")
        return redirect(url_for('index'))

    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    try:
        conn = get_db_connection()
        cur  = conn.cursor()

        # 1) Total de consultas
        if start_date and end_date:
            cur.execute(
                "SELECT COUNT(*) FROM consultas WHERE fecha BETWEEN %s AND %s",
                (start_date, end_date)
            )
        else:
            cur.execute("SELECT COUNT(*) FROM consultas")
        total_consultas = cur.fetchone()[0]

        # 2) Detalle día a día
        if start_date and end_date:
            cur.execute("""
                SELECT DATE(fecha) AS fecha, COUNT(*) AS total
                FROM consultas
                WHERE fecha BETWEEN %s AND %s
                GROUP BY DATE(fecha)
                ORDER BY DATE(fecha)
            """, (start_date, end_date))
        else:
            cur.execute("""
                SELECT DATE(fecha) AS fecha, COUNT(*) AS total
                FROM consultas
                GROUP BY DATE(fecha)
                ORDER BY DATE(fecha)
            """)
        report_rows = cur.fetchall()  # lista de tuplas (fecha, total)

        cur.close()
        conn.close()

    except Exception as e:
        print("Error al generar reporte PDF:", e)
        flash("Error al generar el reporte PDF.", "danger")
        return redirect(url_for('reportes'))

    # Construyo un array de pares para la tabla
    report = [
        (row[0].strftime("%Y-%m-%d") if hasattr(row[0], 'strftime') else row[0], row[1])
        for row in report_rows
    ]

    data = {
        'total_consultas': total_consultas,
        'start_date': start_date,
        'end_date': end_date,
        'report': report
    }

    html = render_template('reportes_pdf.html', data=data, user_name=session.get('user_name'))
    pdf  = HTML(string=html).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reportes.pdf'
    return response

@app.before_request
def clear_session_on_new_start():
    # Si en la sesión no se ha guardado la hora de inicio, o si es distinta a la actual, limpia la sesión.
    if session.get('app_start_time') != app.config['APP_START_TIME']:
        session.clear()
        # Guarda la hora de inicio actual en la sesión para futuras verificaciones.
        session['app_start_time'] = app.config['APP_START_TIME']
@app.route('/ver_consulta/<int:id>')
def ver_consulta(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "SELECT id, consulta, respuesta, fecha FROM consultas WHERE id = %s"
        cursor.execute(sql, (id,))
        registro = cursor.fetchone()
        cursor.close()
        connection.close()
        if registro:
            return render_template('ver_consulta.html', registro=registro, user_name=session.get('user_name'))
        else:
            flash("Consulta no encontrada.")
            return redirect(url_for('historial'))
    except Exception as e:
        print("Error al obtener consulta:", e)
        flash("Error al cargar la consulta.")
        return redirect(url_for('historial'))
@app.route('/borrar_consulta/<int:id>', methods=['GET', 'POST'])
def borrar_consulta(id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "DELETE FROM consultas WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
        cursor.close()
        connection.close()
        flash("Consulta borrada correctamente.")
    except Exception as e:
        print("Error al borrar consulta:", e)
        flash("Error al borrar la consulta.")
    return redirect(url_for('historial'))

@app.route('/admin/busqueda', methods=['GET'])
def admin_busqueda():
    # Obtener parámetros de búsqueda desde la URL
    keyword = request.args.get('keyword', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    # Si tu base de datos almacena la especie, podrías agregar:
    # especie = request.args.get('especie', '')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # Construir la consulta de forma dinámica
        query = "SELECT consulta, respuesta, fecha FROM consultas WHERE 1=1"
        params = []
        if keyword:
            query += " AND consulta LIKE %s"
            params.append(f"%{keyword}%")
        if start_date and end_date:
            query += " AND fecha BETWEEN %s AND %s"
            params.extend([start_date, end_date])
        # Si se manejara la especie (suponiendo que hay una columna 'especie' en la tabla consultas):
        # if especie:
        #     query += " AND especie = %s"
        #     params.append(especie)
        query += " ORDER BY fecha DESC"
        cursor.execute(query, params)
        registros = cursor.fetchall()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error en búsqueda avanzada:", e)
        flash("Error en la búsqueda.")
        registros = []
    return render_template('admin_busqueda.html', registros=registros)
def obtener_diagnostico_sugerido(sintomas_usuario, enfermedades):
    mejor_match = None
    mayor_coincidencias = 0
    
    for enfermedad in enfermedades:
        sintomas_enfermedad = enfermedad["sintomas"].lower().split(", ")
        coincidencias = sum(1 for sintoma in sintomas_usuario if sintoma.lower() in sintomas_enfermedad)

        if coincidencias > mayor_coincidencias:
            mayor_coincidencias = coincidencias
            mejor_match = enfermedad["nombre"]
    
    return mejor_match
# ——————————————————————————————
# RUTAS CRUD PARA USUARIOS (solo admins)
# ——————————————————————————————

def is_admin():
    return session.get('user_role', '').lower() == 'administrativo'

@app.route('/admin/usuarios')
def admin_usuarios():
    if 'user_id' not in session or not is_admin():
        flash("Acceso denegado.")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur  = conn.cursor()
    # Leemos y desencriptamos cada campo
    cur.execute("""
        SELECT 
          id,
          CAST(AES_DECRYPT(nombre, 'mi_clave_secreta') AS CHAR)  AS nombre,
          CAST(AES_DECRYPT(email,  'mi_clave_secreta') AS CHAR)  AS email,
          CAST(AES_DECRYPT(rol,    'mi_clave_secreta') AS CHAR)  AS rol
        FROM usuarios
        ORDER BY id
    """)
    usuarios = cur.fetchall()  # Lista de tuplas (id, nombre, email, rol)
    cur.close()
    conn.close()
    return render_template('admin_usuarios.html', usuarios=usuarios, user_name=session.get('user_name'))

@app.route('/admin/usuarios/agregar', methods=['GET', 'POST'])
def admin_agregar_usuario():
    if 'user_id' not in session or not is_admin():
        flash("Acceso denegado.")
        return redirect(url_for('login'))

    errors = {}  # Diccionario para los errores

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        rol = request.form['rol']
        pwd = request.form['password']

        if not (nombre and email and rol and pwd):
            errors['nombre'] = 'Completa todos los campos.'
            errors['email'] = 'Completa todos los campos.'
            errors['rol'] = 'Completa todos los campos.'
            errors['password'] = 'Completa todos los campos.'
            return render_template('admin_usuario_form.html', accion="Agregar", usuario=request.form, errors=errors, user_name=session.get('user_name'))

        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar si ya existe un usuario con el mismo nombre o email
        cur.execute("""
            SELECT id FROM usuarios
            WHERE AES_DECRYPT(nombre, 'mi_clave_secreta') = %s
               OR AES_DECRYPT(email, 'mi_clave_secreta') = %s
        """, (nombre, email))
        duplicado = cur.fetchone()
        if duplicado:
            errors['nombre'] = 'Ya existe un usuario con ese nombre.'
            errors['email'] = 'Ya existe un usuario con ese correo electrónico.'
            cur.close()
            conn.close()
            return render_template('admin_usuario_form.html', accion="Agregar", usuario=request.form, errors=errors, user_name=session.get('user_name'))

        try:
            cur.execute("""
                INSERT INTO usuarios (nombre, email, rol, password)
                VALUES (
                    AES_ENCRYPT(%s, 'mi_clave_secreta'),
                    AES_ENCRYPT(%s, 'mi_clave_secreta'),
                    AES_ENCRYPT(%s, 'mi_clave_secreta'),
                    AES_ENCRYPT(%s, 'mi_clave_secreta')
                )
            """, (nombre, email, rol, pwd))
            conn.commit()
            flash("Usuario agregado.", "success")
        except Exception as e:
            print("Error al agregar usuario:", e)
            flash("No se pudo agregar el usuario.", "danger")
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('admin_usuarios'))

    return render_template('admin_usuario_form.html', accion="Agregar", usuario={}, errors=errors, user_name=session.get('user_name'))


@app.route('/admin/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
def admin_editar_usuario(usuario_id):
    if 'user_id' not in session or not is_admin():
        flash("Acceso denegado.")
        return redirect(url_for('login'))

    errors = {}  # Diccionario para los errores
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        rol = request.form['rol']
        pwd = request.form.get('password')  # opcional

        if not (nombre and email and rol):
            errors['nombre'] = 'Nombre, email y rol son obligatorios.'
            errors['email'] = 'Nombre, email y rol son obligatorios.'
            errors['rol'] = 'Nombre, email y rol son obligatorios.'
            return render_template('admin_usuario_form.html', accion="Editar", usuario=request.form, errors=errors, user_name=session.get('user_name'))

        # Validar duplicado (excluyendo el propio usuario)
        cur.execute("""
            SELECT id FROM usuarios
            WHERE (AES_DECRYPT(nombre, 'mi_clave_secreta') = %s
                OR AES_DECRYPT(email, 'mi_clave_secreta') = %s)
              AND id != %s
        """, (nombre, email, usuario_id))
        duplicado = cur.fetchone()
        if duplicado:
            errors['nombre'] = 'Ya existe otro usuario con ese nombre.'
            errors['email'] = 'Ya existe otro usuario con ese correo electrónico.'
            cur.close()
            conn.close()
            usuario = {
                'id': usuario_id,
                'nombre': nombre,
                'email': email,
                'rol': rol
            }
            return render_template('admin_usuario_form.html', accion="Editar", usuario=usuario, errors=errors, user_name=session.get('user_name'))

        # Construir el UPDATE dinámico
        sql = """
            UPDATE usuarios SET
                nombre = AES_ENCRYPT(%s, 'mi_clave_secreta'),
                email = AES_ENCRYPT(%s, 'mi_clave_secreta'),
                rol = AES_ENCRYPT(%s, 'mi_clave_secreta')
        """
        params = [nombre, email, rol]

        if pwd:
            sql += ", password = AES_ENCRYPT(%s, 'mi_clave_secreta')"
            params.append(pwd)

        sql += " WHERE id = %s"
        params.append(usuario_id)

        try:
            cur.execute(sql, tuple(params))
            conn.commit()
            flash("Usuario actualizado.", "success")
        except Exception as e:
            print("Error al actualizar usuario:", e)
            flash("No se pudo actualizar el usuario.", "danger")
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('admin_usuarios'))

    # GET = leer datos actuales
    cur.execute("""
        SELECT
            CAST(AES_DECRYPT(nombre, 'mi_clave_secreta') AS CHAR),
            CAST(AES_DECRYPT(email, 'mi_clave_secreta') AS CHAR),
            CAST(AES_DECRYPT(rol, 'mi_clave_secreta') AS CHAR)
        FROM usuarios WHERE id = %s
    """, (usuario_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        flash("Usuario no encontrado.", "warning")
        return redirect(url_for('admin_usuarios'))

    usuario = {
        'id': usuario_id,
        'nombre': row[0],
        'email': row[1],
        'rol': row[2]
    }

    return render_template('admin_usuario_form.html', accion="Editar", usuario=usuario, errors=errors, user_name=session.get('user_name'))

@app.route('/admin/usuarios/eliminar/<int:usuario_id>', methods=['POST'])
def admin_eliminar_usuario(usuario_id):
    if 'user_id' not in session or not is_admin():
        flash("Acceso denegado.")
        return redirect(url_for('login'))
    conn = get_db_connection()
    cur  = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        flash("Usuario eliminado.")
    except Exception as e:
        print("Error al eliminar usuario:", e)
        flash("No se pudo eliminar el usuario.")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('admin_usuarios'))
if __name__ == '__main__':
    app.run(debug=True)
