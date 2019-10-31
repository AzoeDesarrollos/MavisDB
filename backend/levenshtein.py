def levenshtein(a, b):
    """Calculates the Levenshtein distance between a and b."""
    n, m = len(a), len(b)
    if n <= m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def probar_input(item, palabras):
    """Compruba que el input sea válido, utilizando la distancia Levenshtein

    Esta función fue extraída de un documento en PHP, todos los comentarios
    se refeieren a aquel dcumento"""
    cercanas = {}
    # la distancia mas corta no ha sido encontrada, aún
    dist = -1
    # loopea por las palabras hasta encontrar la mas cercana
    for palabra in palabras:
        # calcula la distancia entre la palabra buscada, y la palabra actual
        lev = levenshtein(item, palabra)
        cercanas[palabra] = lev

        if lev <= dist or dist < 0:
            # establecer la coincidencia más cercana y la distancia más corta
            dist = lev

    output = {}
    for key in cercanas:
        value = cercanas[key]
        if cercanas[key] <= dist:
            if value not in output:
                output[value] = []
            if key not in output[value]:
                output[value].append(key)

    return output


def compare_by_lenght(item, palabras):
    k = []
    v = 0
    for i, palabra in enumerate(palabras):
        k.append([palabra, 0])
        if len(palabra) < len(item):
            a, b = palabra, item
        else:
            a, b = item, palabra

        for j, letter in enumerate(a):
            if b[j] == letter:
                k[i][1] += 1
        if k[i][1] > v:
            v = k[i][1]

    f = []
    for o in k:
        if o[1] >= v:
            f.append(o[0])

    return f
