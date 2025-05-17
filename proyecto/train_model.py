import pickle
from collections import Counter
import pymysql
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import accuracy_score

def get_db_connection():
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        db="chatbot_veterinario",
        charset="utf8mb4",
        connect_timeout=5
    )

def actualizar_modelo():
    """
    Consulta todas las enfermedades, extrae sus síntomas,
    entrena un pipeline TF-IDF + LogisticRegression,
    ajustando cv según la clase minoritaria, y guarda modelo.pkl.
    """
    # 1) Cargar datos de enfermedades
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, sintomas FROM enfermedades")
        filas = cursor.fetchall()
    except Exception as e:
        print("Error al obtener datos de enfermedades:", e)
        return
    finally:
        cursor.close()
        conn.close()

    if not filas:
        print("No hay enfermedades para entrenar el modelo.")
        return

    # 2) Preparar X, y y mapeo idx->nombre
    X, y = [], []
    mapeo = {}
    for idx, (enf_id, nombre, sintomas) in enumerate(filas):
        X.append(sintomas)
        y.append(idx)
        mapeo[idx] = nombre

    # 3) Usar StratifiedKFold para asegurar que cada clase esté representada proporcionalmente
    kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # 4) Definir pipeline y grilla
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2))),
        ('clf', LogisticRegression(solver='liblinear', max_iter=1000, class_weight='balanced'))
    ])
    
    param_grid = {
        'tfidf__max_df': [0.75, 1.0],
        'clf__C': [0.1, 1, 10]
    }

    # 5) Intentar grid search con validación cruzada estratificada
    try:
        grid = GridSearchCV(pipeline, param_grid, cv=kf)
        grid.fit(X, y)
        best = grid.best_estimator_
        print("🏆 Mejor score CV:", grid.best_score_)
    except ValueError as e:
        print("⚠️ GridSearchCV falló:", e)
        print("→ Entrenando sin validación cruzada...")
        pipeline.fit(X, y)
        best = pipeline

    # 6) Añadir mapeo al pipeline y guardar
    best.mapeo_enfermedades = mapeo
    with open('modelo.pkl', 'wb') as f:
        pickle.dump(best, f)
    print("✅ Modelo actualizado y guardado en 'modelo.pkl'")
