from .resources import read_csv, is_empty, trim, trim2
from backend.levenshtein import probar_input, compare_by_lenght
from os import path, getcwd, listdir
import openpyxl


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


def process_devir_xlsx(ruta):
    top = []
    bottom = []
    document = openpyxl.load_workbook(ruta)
    for n_hoja in document.sheetnames:
        rows = list(document[n_hoja].rows)
        for row in rows[9:]:
            if type(row[0].value) is int:
                a = trim2(row[:5])

                if len(a) > 1:
                    if len(a) < 6:
                        a.extend([''] * (6 - len(a)))
                    top.append(a)

            if type(row[6].value) is int:
                b = trim2(row[6:])
                if len(b) > 1:
                    if len(b) < 6:
                        b.extend([''] * (6 - len(b)))
                    bottom.append(b)

    document.close()
    table = top + bottom
    tabla = []
    for j, row in enumerate(table):
        row = row[1:]
        tabla.append({
            'codigo': j,
            'nombre': row[0].upper(),
            'precio_siva': row[1],
            'precio': row[2],
            'pedido': row[3],
            'otro': row[4],
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
            'ISBN': row[4],
            'EAN': row[5],
            'ADENDUM': row[6],
            'editorial': row[7],
            'autor': row[8]
        })
    return table


def process_sd_dist_xlsx(ruta):
    tabla = []
    document = openpyxl.load_workbook(ruta)
    for n_hoja in document.sheetnames:
        hoja = list(document[n_hoja].rows)[5:]
        for fila in hoja:
            if fila[1].value is not None and len(fila[1].value) == 11:
                f = trim2(fila[1:], delete_empty=False)
                fila = f[0:3] + f[5:]
                tabla.append(fila)

    document.close()
    table = []
    for row in tabla:
        n = row[1]
        table.append({
            'codigo': row[0],
            'nombre': n.upper() if type(n) is str else str(n).upper(),
            'precio': row[2],
            'ISBN': row[3],
            'EAN': row[4],
            'ADENDUM': row[5],
            'editorial': row[6],
            'autor': row[7]
        })
    return table


def process_ivrea(ruta):
    tabla = []
    for row in read_csv(ruta)[9:]:
        if row[2] != '':
            tabla.append({
                'codigo': row[1],
                'nombre': row[2].lstrip().rstrip(),
                'ISBN': row[3],
                'EAN': row[4].lstrip().rstrip(),
                'ADENDUM': row[5],
                'precio': float(row[6].replace(',', '.').strip(' $')),
                'agotado': 1 if len(row[8]) else 0
            })
    return tabla


def process_ivrea_xlsx(ruta):
    tabla = []
    document = openpyxl.load_workbook(ruta)
    for n_hoja in document.sheetnames:
        rows = list(document[n_hoja].rows)
        for r in rows[9:]:
            if r[2].value is not None:
                isbn = '-'
                if type(r[3].value) is int:
                    isbn = str(r[3].value)
                elif r[3].value is not None:
                    isbn = ''.join(r[3].value.split('-'))
                tabla.append({
                    'código': r[1].value,
                    'nombre': r[2].value.lstrip().rstrip(),
                    'ISBN': isbn,
                    'EAN': r[4].value,
                    'ADENDUM': r[5].value,
                    'precio': float(r[6].value),
                    'agotado': 1 if r[8].value is not None else 0
                })

    document.close()
    return tabla


def process_plan(ruta):
    tabla = []
    for row in read_csv(ruta)[9:]:
        if row[0] != '':
            t = row[3].upper()
            t = t.lstrip().rstrip().split(' - ')[0] if 'SIN STOCK' in t else t.lstrip().rstrip()
            tabla.append({
                'codigo': row[0],
                'nombre': t,
                'ISBN': row[2],
                'precio': float(row[4].replace(',', '.').strip(' $')),
                'agotado': 1 if 'Sin Stock' in row[3].title() else 0
            })

    return tabla


def process_plan_xlsx(ruta):
    tabla = []
    document = openpyxl.load_workbook(ruta)
    for n_hoja in document.sheetnames:
        rows = list(document[n_hoja].rows)
        for r in rows[9:]:
            if r[0].value is not None:
                t = r[3].value.upper()
                n = t.split(' - ')[0] if 'SIN STOCK' in t else t
                n.strip()

                isbn = '-'
                if type(r[2].value) is int:
                    isbn = str(r[2].value)
                elif r[2].value is not None:
                    isbn = ''.join(r[2].value.split('-'))

                tabla.append({
                    'codigo': r[0].value,
                    'nombre': n,
                    'ISBN': isbn,
                    'precio': float(r[6].value),
                    'agotado': 1 if 'SIN STOCK' in t else 0
                })

    document.close()
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
        if file.endswith('.csv'):
            tablas.append(process_devir(route))
        else:
            tablas.append(process_devir_xlsx(route))
    elif 'SD' in file:
        if file.endswith('.csv'):
            tablas.append(process_sd_dist(route))
        else:
            tablas.append(process_sd_dist_xlsx(route))
    elif 'IVREA' in file:
        if file.endswith('.csv'):
            tablas.append(process_ivrea(route))
        else:
            tablas.append(process_ivrea_xlsx(route))
    elif 'Plan' in file:
        if file.endswith('.csv'):
            tablas.append(process_plan(route))
        else:
            tablas.append(process_plan_xlsx(route))


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
