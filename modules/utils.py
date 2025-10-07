def format_set(s):
    return ", ".join(map(str, sorted(s))) if s else "Ø"

# Nota: la validación de pertenencia se realiza con elements_not_in_universe()


def find_duplicates_in_csv(text):
    """Devuelve un conjunto con los elementos duplicados en una cadena CSV.

    Ejemplo: "1,2,2,3" -> {"2"}
    Se trabaja con tokens de texto para detectar duplicados antes de convertir a set.
    """
    if not text:
        return set()
    tokens = [t.strip() for t in text.split(",") if t.strip() != ""]
    seen = set()
    duplicates = set()
    for token in tokens:
        if token in seen:
            duplicates.add(token)
        else:
            seen.add(token)
    return duplicates


def elements_not_in_universe(universe, subset):
    """Retorna los elementos de 'subset' que NO pertenecen a 'universe'."""
    return set(subset) - set(universe)


