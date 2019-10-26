from backend.eventhandler import EventHandler
from os import getcwd, path
from datetime import datetime
from .widgets import *


class AreaVentas:
    cart = None
    subtotal_acumulado = 0
    total_lbl = None

    @classmethod
    def init(cls):
        EventHandler.register(cls.subtotal, 'Subtotal')
        cls.cart = Cart(643, 31, 900 - 640)
        Label('Adquirido', 643, 10, 900 - 640, just=1)
        cls.total_lbl = Label('Total\n$0.00', 643, 400, 900 - 640, just=1)
        Button(710, 465, 'Cerrar Compra', action=cls.checkout)

    @classmethod
    def subtotal(cls, event):
        cls.subtotal_acumulado += event.data.get('price', 0)
        cls.total_lbl.update_text('Total\n' + '$' + str(cls.subtotal_acumulado), just=1)

    @classmethod
    def checkout(cls):
        now = datetime.now()
        year, month = str(now.year), str(now.month)
        root = path.join(path.join(getcwd(), 'ventas', year, month))

        v = 0
        if path.exists(path.join(root, str(now.day)+'.txt')):
            with open(path.join(root, str(now.day)+'.txt'), 'r') as file:
                for line in file.readlines():
                    if 'Venta' in line:
                        v += 1

        with open(path.join(root, str(now.day)+'.txt'), 'a') as file:
            file.write('Venta #'+str(v)+':'+str(now.hour)+':'+str(now.minute)+':'+str(now.second)+'\n')
            for item in cls.cart.items:
                file.write(item.item.name.title()+'.....$'+str(item.item.price)+'\n')
            file.write('Total: $'+str(cls.subtotal_acumulado)+'\n\n')

        cls.cart.clear()
        cls.total_lbl.update_text('Total\n$0.00', just=1)
