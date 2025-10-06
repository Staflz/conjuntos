def format_set(s):
    return ", ".join(map(str, sorted(s))) if s else "Ø"

def validate_input(u, a, b):
    """Verifica que A y B estén contenidos en U."""
    if not a.issubset(u) or not b.issubset(u):
        raise ValueError("A y B deben ser subconjuntos de U.")


