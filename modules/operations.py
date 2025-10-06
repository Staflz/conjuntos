def parse_set(text):
    """Convierte una cadena como '1,2,3' en un conjunto {1,2,3}"""
    return set(map(int, text.replace(" ", "").split(","))) if text else set()

def union(a, b):
    return a | b

def interseccion(a, b):
    return a & b

def diferencia(a, b):
    return a - b

def diferencia_simetrica(a, b):
    return a ^ b

def complemento(u, a):
    return u - a
