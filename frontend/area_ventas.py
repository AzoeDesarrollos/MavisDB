from backend.eventhandler import EventHandler
from .widgets import *


class AreaVentas:
    cart = []
    subtotal_acumulado = 0
    total_lbl = None

    @classmethod
    def init(cls):
        EventHandler.register(cls.subtotal, 'Subtotal')
        Cart(643, 31, 900 - 640)
        Label('Adquirido', 643, 10, 900-640, just=1)
        cls.total_lbl = Label('Total', 643, 400, 900 - 640, just=1)

    @classmethod
    def subtotal(cls, event):
        cls.subtotal_acumulado += event.data.get('price', 0)
        cls.total_lbl.update_text('Total\n'+'$'+str(cls.subtotal_acumulado), just=1)
