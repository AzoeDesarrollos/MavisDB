from frontend import Renderer, WidgetHandler, COLOR_FONDO, COLOR_TEXTO, ALTO
from frontend.globals.textrect import render_textrect
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from .button import Button
from pygame.sprite import Group
from pygame import font, Rect, Surface, key
from pygame import KMOD_LCTRL, KMOD_CTRL, K_RSHIFT, K_LSHIFT, K_PLUS, K_KP_PLUS
from pygame import K_PAGEDOWN, K_PAGEUP, K_DOWN, K_UP


class Label(BaseWidget):

    def __init__(self, text, x, y, w, size=16):
        self.x, self.y = x, y
        self.f = font.SysFont('Verdana', size)
        self.image = render_textrect(text, self.f, w, COLOR_TEXTO, COLOR_FONDO)
        self.w, self.h = self.image.get_size()
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__()
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)


class LabelList(BaseWidget):
    render = None
    scroll_y = 0
    items = None
    selected_items = None
    salto_de_linea = 0

    def __init__(self, x, y, w, text_h=14):
        self.x, self.y, self.w, self.h = x, y, w, 0
        self.text_h = text_h
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.image = Surface(self.rect.size)
        self.items = []
        self.selected_items = Group()
        super().__init__()
        EventHandler.register(self.show, 'show_text')
        WidgetHandler.add_widget(self, 1)

    def show(self, event):
        self.clear()
        WidgetHandler.set_active(self)
        self.fill(event.data.get('text'))

    def clear(self):
        for item in self.items:
            Renderer.del_widget(item)
            WidgetHandler.del_widget(item)
        self.items.clear()
        self.h = 0

    def fill(self, texts):
        for text in texts:
            item = LabelListItem(self, text, self.y+self.h, self.text_h)
            self.h += item.h
            self.items.append(item)
        self.image = Surface((self.w, self.h))
        self.dirty = 1

    def on_keydown(self, tecla):
        if tecla == K_DOWN:
            self.scroll(-self.salto_de_linea)
        elif tecla == K_UP:
            self.scroll(+self.salto_de_linea)
        elif tecla == K_PAGEDOWN:
            self.scroll(-self.salto_de_linea * 2)
        elif tecla == K_PAGEUP:
            self.scroll(+self.salto_de_linea * 2)
        return False  # the key was not captured

    def on_mousebuttondown(self, button):
        if button == 5:  # down
            self.scroll(-self.salto_de_linea)
        elif button == 4:  # up
            self.scroll(+self.salto_de_linea)

    def scroll(self, direction):
        if self.items[0].y + direction <= self.y and self.items[-1].rect.bottom + direction > ALTO:
            for item in self.items:
                item.scroll(direction)

        for item in self.items:
            if item.y < self.y:
                Renderer.del_widget(item)
                WidgetHandler.del_widget(item)
            else:
                Renderer.add_widget(item)
                WidgetHandler.add_widget(item)

    def deselegir_todo(self):
        for item in self.items:
            item.ser_deselegido()

    def select(self, item):
        self.selected_items.add(item)

    def deselect(self, item):
        self.selected_items.remove(item)

    def select_many(self, item):
        if len(self.items):
            a = self.items.index(self.selected_items.sprites()[0])
            b = self.items.index(item)

            if a < b:
                lo = a
                hi = b
            else:
                hi = a
                lo = b

            for item in self.items[lo:hi]:
                item.ser_elegido()

    def update(self):
        self.image.fill(COLOR_FONDO)
        self.dirty = 1


class LabelListItem(BaseWidget):
    is_selected = False

    def __init__(self, parent, text, y, h):
        self.item = Item(text)
        self.name = self.item.name + '.Label'

        self.fuente = font.SysFont('Verdana', h)
        texto = self.item.shelf(precio='precio' in text, isbn='ISBN' in text)
        self.altura_del_texto = self.fuente.get_height()
        self.img_sel = render_textrect(texto, self.fuente, parent.w, [255, 255, 255], COLOR_FONDO)
        self.img_uns = render_textrect(texto, self.fuente, parent.w, [0, 0, 0], COLOR_FONDO)
        self.image = self.img_uns
        self.w, self.h = self.image.get_size()
        self.x, self.y = parent.x, y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        super().__init__(parent)
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def on_mousebuttondown(self, button):
        mods = key.get_mods()
        ctrl = mods & KMOD_CTRL or mods & KMOD_LCTRL
        shift = mods & K_LSHIFT or mods & K_RSHIFT
        if button == 1 and self.is_selected:
            self.parent.deselegir_todo()
            self.ser_elegido()
        elif button == 1 and not self.is_selected:
            if shift:
                self.ser_elegido()
                self.parent.select_many(self)
            elif not ctrl:
                self.parent.deselegir_todo()
            self.ser_elegido()
        else:
            self.parent.on_mousebuttondown(button)

    def on_keydown(self, tecla):
        self.parent.on_keydown(tecla)

    def scroll(self, dy):
        self.rect.move_ip(0, dy)
        self.y += dy
        self.dirty = 1

    def ser_elegido(self):
        self.image = self.img_sel
        self.is_selected = True
        self.parent.select(self)
        self.dirty = 1

    def ser_deselegido(self):
        self.image = self.img_uns
        self.is_selected = False
        self.parent.deselect(self)
        self.dirty = 1


class Item:
    name = ''
    price = 0
    isbn = None

    def __init__(self, data):
        self.name = data['nombre']
        self.price = data.get('precio', 0)
        self.isbn = data.get('ISBN', None)

    def shelf(self, precio=True, isbn=False):
        string = self.name.title()
        if precio:
            string += ' Precio: $' + str(self.price)
        if isbn:
            if self.isbn is not None:
                string += ' ISBN: ' + str(self.isbn)
            else:
                string += ' ISBN: -'

        return string

    def __repr__(self):
        return self.name.title()


class CartableLabelList(LabelList):

    def fill(self, texts):
        for text in texts:
            item = CartableLabelListItem(self, text, self.y+self.h)
            self.h += item.h
            self.items.append(item)
        self.image = Surface((self.w, self.h))
        self.dirty = 1


class CartableLabelListItem(LabelListItem):
    def __init__(self, parent, text, y, text_h=14):
        super().__init__(parent, text, y, text_h)
        self.x = parent.x + 20
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        self.sell_button = Button(0, self.y, '+', action=self.export, font_size=10)
        self.sell_button.hide()

    def on_keydown(self, tecla):
        if not self.parent.on_keydown(tecla):
            if tecla in [K_PLUS, K_KP_PLUS]:
                self.export()

    def export(self):
        EventHandler.trigger('AddToCart', self.name, {'item': self.item})

    def ser_elegido(self):
        super().ser_elegido()
        self.sell_button.show()

    def ser_deselegido(self):
        super().ser_deselegido()
        self.sell_button.hide()
