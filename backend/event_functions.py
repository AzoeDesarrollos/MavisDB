from .database import tablas


def select_one(column, table, key, value):
    tabla = tablas[table]
    for row in tabla:
        if row[key] == value:
            return row[column]


def select_many(column, key, value):
    results = []
    for tabla in tablas:
        for row in tablas[tabla]:
            if key in row[value]:
                results.append({'nombre': row['nombre'], 'precio': row[column]})
    return results


def devolver_todos():
    return [i['nombre'] for i in tablas['devir']]+[j['nombre'] for j in tablas['sd_dist']]


__all__ = [
    'devolver_todos',
    'select_many'
    ]
