from .database import tablas


def select_many(key, value, columns):
    results = []
    for tabla in tablas:
        for row in tabla:
            if key in row[value]:
                d = {'nombre': row['nombre']}
                for column in columns:
                    if column in row:
                        d[column] = row[column]
                results.append(d)
    results.sort(key=lambda o: o['nombre'])
    return results


def devolver_todos():
    return [i['nombre'] for i in tablas['devir']]+[j['nombre'] for j in tablas['sd_dist']]


__all__ = [
    'devolver_todos',
    'select_many'
    ]
