from backend.eventhandler import EventHandler
from .widgets import *


class AreaVentas:
    cart = []

    @classmethod
    def init(cls, x):
        EventHandler.register(cls.add_item, 'AddToCart')
        LabelList(x, 0, 900 - 640, 12)

    @classmethod
    def add_item(cls, event):
        item = event.data['item']
        cls.cart.append(item)
        print(cls.cart)

    @classmethod
    def show_items(cls):
        for item in cls.cart:
            pass
