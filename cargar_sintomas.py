import pymysql
import unicodedata
import os

def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def get_db_connection():
    """
    Establece una conexión a la base de datos leyendo las credenciales
    de las variables de entorno, con valores por defecto para desarrollo local.
    """
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        db=os.environ.get("DB_NAME", "chatbot_veterinario"),
        charset="utf8mb4",
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,  # Opcional: devuelve dicts en lugar de tuplas
        autocommit=True                          # Opcional: no necesitas hacer conn.commit()
    )

def cargar_diccionario_sinonimos():
    """
    Carga un diccionario sinónimo_normalizado -> síntoma_canonical.
    Por ejemplo: 'fiebre' -> 'fiebre', 'tos seca' -> 'tos seca'.
    Si hay error de conexión, devuelve un dict vacío.
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute("SELECT sintomas FROM enfermedades")
        registros = cur.fetchall()
    except Exception as e:
        print("Error al cargar sinónimos desde BD:", e)
        return {}
    finally:
        if cur:
            try: cur.close()
            except: pass
        if conn:
            try: conn.close()
            except: pass

    sinonimos = {}
    for row in registros:
        sintomas_csv = row.get("sintomas") if isinstance(row, dict) else row[0]
        if not sintomas_csv:
            continue
        for sin in (s.strip().lower() for s in sintomas_csv.split(',') if s.strip()):
            sin_norm = normalizar_texto(sin)
            sinonimos[sin_norm] = sin_norm

    return sinonimos

def cargar_lista_sintomas():
    """
    Carga una lista única de síntomas desde la BD.
    Si hay error, devuelve lista vacía.
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        cur.execute("SELECT sintomas FROM enfermedades")
        registros = cur.fetchall()
    except Exception as e:
        print("Error al cargar síntomas desde BD:", e)
        return []
    finally:
        if cur:
            try: cur.close()
            except: pass
        if conn:
            try: conn.close()
            except: pass

    lista_sintomas = set()
    for row in registros:
        sintomas_csv = row.get("sintomas") if isinstance(row, dict) else row[0]
        if not sintomas_csv:
            continue
        for sin in (s.strip().lower() for s in sintomas_csv.split(',') if s.strip()):
            lista_sintomas.add(sin)

    return list(lista_sintomas)
