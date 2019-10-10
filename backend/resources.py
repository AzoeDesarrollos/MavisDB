from .eventhandler import EventHandler
from pygame import quit
from sys import exit
import csv
import os


class MyCSV(csv.excel):
    delimiter = ';'


def read_csv(ruta):
    """Lee archivos CSV y los devuelve como una lista."""

    table = []
    with open(ruta, encoding='windows-1252') as file:
        data = csv.reader(file, dialect=MyCSV)
        for row in data:
            table.append(row)
        if len(table) == 1:
            table = table[0]

    return table


def write_csv(ruta, tabla):
    with open(ruta, 'w+t', newline='') as csvfile:
        fieldnames = list(tabla[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=MyCSV)
        writer.writeheader()
        writer.writerows(tabla)


def is_empty(line):
    return all(line[i] == '' for i in range(len(line)))


def trim(line, delete_empty=True, newline=True):
    if newline:
        line = [''.join(item.splitlines()) for item in line]
    if delete_empty:
        return [item.strip() for item in line if item != '']
    else:
        return [item.strip() for item in line]


def salir_handler(event):
    quit()
    data = event.data.get('mensaje', '')
    print('Saliendo...\nStatus: ' + data)
    exit()


EventHandler.register(salir_handler, 'salir')

if 'data' not in os.listdir(os.getcwd()):
    os.mkdir(os.path.join(os.getcwd(), 'data'))
