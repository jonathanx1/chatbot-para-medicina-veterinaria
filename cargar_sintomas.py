import pymysql
import unicodedata
import os
def normalizar_texto(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def get_db_connection():
    return pymysql.connect(
        host        = os.environ.get("DB_HOST", "127.0.0.1"),
        port        = int(os.environ.get("DB_PORT", 3306)),
        user        = os.environ.get("DB_USER", "root"),
        password    = os.environ.get("DB_PASSWORD", ""),
        db          = os.environ.get("DB_NAME", "chatbot_veterinario"),
        charset     = "utf8mb4",
        connect_timeout = 5
    )

def cargar_diccionario_sinonimos():
    """
    Carga un diccionario sinónimo_normalizado -> síntoma_canonical.
    Por ejemplo: 'fiebre' -> 'fiebre', 'tos seca' -> 'tos seca'.
    """
    try:
        conn = get_db_connection()
        cur  = conn.cursor()
        # Solo necesitamos la columna 'sintomas'
        cur.execute("SELECT sintomas FROM enfermedades")
        registros = cur.fetchall()
    except Exception as e:
        print("Error al cargar sinónimos desde BD:", e)
        return {}
    finally:
        cur.close()
        conn.close()

    sinonimos = {}
    for (sintomas_csv,) in registros:
        if not sintomas_csv:
            continue
        for sin in [s.strip().lower() for s in sintomas_csv.split(',') if s.strip()]:
            sin_norm = normalizar_texto(sin)
            # Mapear cada sinónimo a sí mismo (el síntoma)
            sinonimos[sin_norm] = sin_norm

    return sinonimos


def cargar_lista_sintomas():
    """
    Carga una lista única de síntomas desde la BD.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT sintomas FROM enfermedades")
        registros = cur.fetchall()
    except Exception as e:
        print("Error al cargar síntomas desde BD:", e)
        return []
    finally:
        cur.close()
        conn.close()

    lista_sintomas = set()
    for sintomas_csv, in registros:
        if not sintomas_csv:
            continue
        sintomas = [s.strip().lower() for s in sintomas_csv.split(',') if s.strip()]
        lista_sintomas.update(sintomas)

    return list(lista_sintomas)
