def parse_set(text):
    """Convierte una cadena como '1, 2, 3' en un conjunto {1,2,3} con enteros >= 0.

    Reglas:
    - Acepta espacios múltiples alrededor de comas (se ignoran).
    - Rechaza tokens vacíos (por ejemplo, ",,") y caracteres no numéricos.
    - Solo permite enteros no negativos (>= 0).
    """
    if not text:
        return set()
    tokens = [t.strip() for t in text.split(",")]
    if any(t == "" for t in tokens):
        raise ValueError("Formato inválido: evita comas consecutivas o al final.")
    values = set()
    for t in tokens:
        if not t.isdigit():
            raise ValueError("Entrada inválida: solo se permiten enteros no negativos (>= 0).")
        values.add(int(t))
    return values

# Operaciones clásicas eliminadas por no uso directo en la interfaz actual.


def operate_binary_by_universe(universe: set[int], a: set[int], b: set[int], op: str) -> set[int]:
    """Replica la lógica del Java iterando sobre U y evaluando p, q por operador.

    op: 'union' | 'inter' | 'diff_a_b' | 'diff_b_a' | 'sym'
    """
    if not universe:
        return set()
    result = []
    # Mantener un orden determinista basado en U ordenado
    for x in sorted(universe):
        p = x in a
        q = x in b
        if op == 'union':
            if p or q:
                result.append(x)
        elif op == 'inter':
            if p and q:
                result.append(x)
        elif op == 'diff_a_b':
            if p and not q:
                result.append(x)
        elif op == 'diff_b_a':
            if q and not p:
                result.append(x)
        elif op == 'sym':
            if (p and not q) or (q and not p):
                result.append(x)
        else:
            raise ValueError('Operador no soportado')
    return set(result)


def operate_unary_by_universe(universe: set[int], a: set[int], op: str) -> set[int]:
    """Replica la lógica del Java para operador unario (complemento) recorriendo U."""
    if not universe:
        return set()
    result = []
    for x in sorted(universe):
        p = x in a
        if op == 'comp':
            if not p:
                result.append(x)
        else:
            raise ValueError('Operador unario no soportado')
    return set(result)
