import re
import unicodedata
from typing import List, Tuple
from cargar_sintomas import cargar_diccionario_sinonimos

# Patrones de negación mejorados
NEGACION_PATTERNS = [
    r"\b(no|sin|ni|pero no)\s+{sin}\b",
    r"\b(no|sin|ni|pero no)\s+tiene\s+{sin}\b",
    r"\b(no|sin|ni|pero no)\s+presenta\s+{sin}\b",
    r"\b(no|sin|ni|pero no)\s+sufre\s+de\s+{sin}\b",
    r"\b(no|sin|ni|pero no)\s+padece\s+{sin}\b",
    r"\b(sin\s+síntomas\s+de)\s+{sin}\b",
    r"\b(no\s+parece\s+tener)\s+{sin}\b"
]

def normalizar(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Cargamos el diccionario sinónimo -> síntoma canónico
SINONIMO_A_SINTOMA = cargar_diccionario_sinonimos()

def extraer_sintomas_nlp(texto: str) -> Tuple[List[str], List[str]]:
    """
    Devuelve dos listas:
     - síntomas afirmados
     - síntomas negados
    Evita síntomas duplicados si uno ya incluye al otro (ej: 'tos seca' y 'tos').
    """
    txt = normalizar(texto)
    afirmados = []
    negados = []
    usados = set()  # Set de tuplas (start, end) de spans de síntomas ya detectados para evitar solapamientos

    for sin_norm, sint_canon in sorted(SINONIMO_A_SINTOMA.items(), key=lambda x: len(x[0]), reverse=True):
        pat = re.escape(sin_norm)
        # Buscar el síntoma como palabra completa (evita coincidencias parciales)
        match = re.search(rf"\b{pat}\b", txt)
        
        if match:
            span = match.span()
            # Verificar si el span se solapa con alguno ya detectado para evitar duplicados
            if any(start <= span[0] < end or start < span[1] <= end for start, end in usados):
                continue  # Ya cubierto por un síntoma más específico
            
            usados.add(span)
            
            # Verificar negación
            negado = False
            for neg_pat in NEGACION_PATTERNS:
                if re.search(neg_pat.format(sin=pat), txt):
                    if sint_canon not in negados:
                        negados.append(sint_canon)
                    negado = True
                    break
            
            if not negado:
                if sint_canon not in afirmados:
                    afirmados.append(sint_canon)

    return afirmados, negados

# Función para recargar el diccionario dinámicamente
def actualizar_diccionario_sinonimos():
    global SINONIMO_A_SINTOMA
    SINONIMO_A_SINTOMA = cargar_diccionario_sinonimos()
    print("Diccionario de sinónimos actualizado.")
