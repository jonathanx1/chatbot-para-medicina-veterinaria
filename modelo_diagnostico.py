# modelo_diagnostico.py

import os
import pickle
from train_model import actualizar_modelo

MODELO_PATH = 'modelo.pkl'

def cargar_modelo():
    """
    Intenta cargar el modelo entrenado desde MODELO_PATH.
    Si no existe, reentrena uno nuevo y vuelve a intentarlo.
    """
    if not os.path.exists(MODELO_PATH):
        print("⚠️ modelo.pkl no encontrado, entrenando uno nuevo...")
        actualizar_modelo()
    try:
        with open(MODELO_PATH, 'rb') as f:
            modelo = pickle.load(f)
        return modelo
    except Exception as e:
        print("❌ Error al cargar el modelo:", e)
        return None

def predecir_diagnostico(sintomas: list[str], especie: str = None) -> str:
    """
    Recibe una lista de síntomas y, opcionalmente, la especie.
    Devuelve el nombre de la enfermedad predicha.
    """
    texto = " ".join(sintomas)
    modelo = cargar_modelo()
    if modelo is None:
        return "Modelo no disponible"
    try:
        pred = modelo.predict([texto])[0]
        # Si el pipeline trae un atributo con el mapeo de etiquetas:
        if hasattr(modelo, "mapeo_enfermedades"):
            return modelo.mapeo_enfermedades.get(pred, "Desconocido")
        return str(pred)
    except Exception as e:
        print("❌ Error en predecir_diagnostico:", e)
        return "Error en la predicción"
