from .resources import read_csv, is_empty, trim
from backend.levenshtein import probar_input, compare_by_lenght
from os import path, getcwd, listdir


def process_devir(ruta):
    top = []
    bottom = []
    for row in read_csv(ruta):
        if not is_empty(row) and row[0] != '':
            column = row.index('')
            a = trim(row[:column])
            b = trim(row[column + 1:])
            if len(a) > 1:
                if len(a) < 6:
                    a.extend([''] * (6 - len(a)))
                top.append(a)

            if len(b) > 1:
                if len(b) < 6:
                    b.extend([''] * (6 - len(b)))
                bottom.append(b)

    table = top[1:] + bottom[1:]
    tabla = []
    for j, row in enumerate(table):
        row = row[1:]
        for i, value in enumerate(row):
            if value.startswith('$'):
                value = value.replace('.', '').replace(',', '.')
                row[i] = float(value[1:])

        tabla.append({
            'codigo': j,
            'nombre': row[0].upper(),
            'precio_siva': row[1],
            'precio': row[2],
            'pedido': row[3] if row[3] is not '' else None,
            'otro': row[4] if row[4] is not '' else None
            })

    return tabla


def process_sd_dist(ruta):
    tabla = []
    for fila in read_csv(ruta):
        if fila[1] != '' and len(fila[1]) == 11:
            f = trim(fila[1:], delete_empty=False)
            fila = f[0:4] + f[5:]
            tabla.append(fila)

    table = []
    for row in tabla:
        for i, value in enumerate(row):
            if value.startswith('$'):
                value = value.replace('.', '').replace(',', '.')
                row[i] = float(value[1:])
            elif value.endswith('%'):
                row[i] = int(value[:value.index('%')])
        table.append({
            'codigo': row[0],
            'nombre': row[1].upper(),
            'precio': row[2],
            'decuento': row[3],
            'ISBN': row[4],
            'EAN': row[5],
            'ADENDUM': row[6],
            'editorial': row[7],
            'autor': row[8]
            })
    return table


def process_ivrea(ruta):
    tabla = []
    for row in read_csv(ruta)[9:]:
        if row[2] != '':
            tabla.append({
                'codigo': row[1],
                'nombre': row[2].lstrip().rstrip(),
                'isbn': row[3],
                'ean': row[4].lstrip().rstrip(),
                'adendum': row[5],
                'precio': float(row[6].replace(',', '.').strip(' $')),
                'agotado': 1 if len(row[8]) else 0
                })
    return tabla


def process_plan(ruta):
    tabla = []
    for row in read_csv(ruta)[9:]:
        if row[0] != '':
            t = row[3].lstrip().rstrip().split(' - ')[0] if 'Sin Stock' in row[3].title() else row[3].lstrip().rstrip()
            tabla.append({
                'codigo': row[0],
                'nombre': t,
                'isbn': row[2],
                'precio': float(row[4].replace(',', '.').strip(' $')),
                'agotado': 1 if 'Sin Stock' in row[3].title() else 0
                })

    return tabla


def open_table(ruta):
    tabla = []
    datos = read_csv(ruta)
    header = datos[0]
    rows = datos[1:]
    for i, row in enumerate(rows):
        tabla.append({})
        for j, value in enumerate(row):
            head = header[j]
            if head == 'codigo':
                try:
                    value = int(value)
                except ValueError:
                    # sd_dist codes are not numeric.
                    pass
            elif head in ('precio', 'precio_siva', 'descuento'):
                value = float(value)
            tabla[i].update({header[j]: value})
    return tabla


root = getcwd() + '/data'
tablas = []
for file in listdir(root):
    route = path.join(root, file)
    if 'Devir' in file:
        tablas.append(process_devir(route))
    elif 'SD' in file:
        tablas.append(process_sd_dist(route))
    elif 'IVREA' in file:
        tablas.append(process_ivrea(route))
    elif 'Plan' in file:
        tablas.append(process_plan(route))


def select_many(key, columns):
    results = []
    for tabla in tablas:
        for row in tabla:
            if key in row['nombre']:
                d = {'nombre': row['nombre']}
                for column in columns:
                    if column in row:
                        d[column] = row[column]
                results.append(d)

    if not len(results):
        cercana = {}
        for tabla in tablas:
            names = [row['nombre'] for row in tabla]
            cercana.update(probar_input(key, names))

        for c in compare_by_lenght(key, cercana.pop(min(cercana))):
            results.extend(select_many(c, columns))

    results.sort(key=lambda o: o['nombre'])
    return results
