from backend.eventhandler import EventHandler
from os import getcwd, path
from datetime import datetime
from .widgets import *


class AreaVentas:
    cart = None
    subtotal_acumulado = 0
    total_lbl = None
    ultima_chk = None

    @classmethod
    def init(cls):
        EventHandler.register(cls.subtotal, 'Subtotal')
        cls.cart = Cart(643, 31, 900 - 640)
        Label('Adquirido', 643, 10, 900 - 640, just=1)
        cls.total_lbl = Label('Total\n$0.00', 643, 400, 900 - 640, just=1)
        b = Button(710, 465, 'Cerrar Compra', action=cls.checkout)
        cls.ultima_chk = Checkbox(b.rect.right + 12, b.rect.centery, 'CheckUltimaComra')
        chk = cls.ultima_chk
        Label('Última', chk.rect.right + 3, chk.rect.top - 2, size=12)

    @staticmethod
    def open_sales_file(mode):
        now = datetime.now()
        year, month = str(now.year), str(now.month)
        root = path.join(path.join(getcwd(), 'ventas', year, month))
        if path.exists(path.join(root, str(now.day) + '.txt')):
            return open(path.join(root, str(now.day) + '.txt'), mode)

    @classmethod
    def total_del_dia(cls):
        total = 0
        with cls.open_sales_file('r') as file:
            for line in file.readlines():
                if "Total" in line:
                    total += float(line.strip('Total:$ '))
        return total

    @classmethod
    def subtotal(cls, event):
        cls.subtotal_acumulado += event.data.get('price', 0)
        cls.total_lbl.update_text('Total\n' + '$' + str(cls.subtotal_acumulado), just=1)

    @classmethod
    def ultima_compra(cls):
        total = cls.total_del_dia()
        with cls.open_sales_file('a') as file:
            file.write('\n**TOTAL DEL DÍA: $' + str(total))

    @classmethod
    def checkout(cls):
        v = 0
        now = datetime.now()
        with cls.open_sales_file('r') as file:
            for line in file.readlines():
                if 'Venta' in line:
                    v += 1

        with cls.open_sales_file('a') as file:
            file.write('Venta #' + str(v) + ':' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + '\n')
            for item in cls.cart.items:
                file.write(item.item.name.title() + '.....$' + str(item.item.price) + '\n')
            file.write('Total: $' + str(cls.subtotal_acumulado) + '\n\n')

        cls.cart.clear()
        cls.total_lbl.update_text('Total\n$0.00', just=1)
        cls.subtotal_acumulado = 0

        if cls.ultima_chk.state:
            cls.ultima_compra()
            EventHandler.trigger('salir', 'AreaVentas', {})
