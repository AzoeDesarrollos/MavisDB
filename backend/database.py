from .resources import read_cvs, is_empty, trim
from os import path, getcwd


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
            'nombre': row[0],
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
            'nombre': row[1],
            'precio': row[2],
            'decuento': row[3],
            'ISBN': row[4],
            'EAN': row[5],
            'ADENDUM': row[6],
            'editorial': row[7],
            'autor': row[8]
            })
    return table


def open_table(ruta):
    tabla = []
    datos = read_cvs(ruta)
    header = datos[0]
    rows = datos[1:]
    for i, row in enumerate(rows):
        tabla.append({})
        for j, value in enumerate(row):
                head = header[j]
                if head == 'codigo' :
                    try:
                        value = int(value)
                    except ValueError:
                        # sd_dist codes are not numeric.
                        pass
                elif head in ('precio','precio_siva', 'descuento'):
                    value = float(value)
                tabla[i].update({header[j]:value})
    return tabla


tablas = {
    'devir': process_devir(path.join(getcwd(), 'data/Lista_de_Precios_Devirb.csv')),
    'sd_dist': process_sd_dist(path.join(getcwd(), 'data/LISTADO_SD_DISTRIBUCIONES_19_07_2019b.csv'))
    }

__all__ = [
    'tablas'
    ]
