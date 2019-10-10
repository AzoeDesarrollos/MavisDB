from pygame import Surface, font, key, draw, K_LSHIFT, K_RSHIFT, KMOD_CAPS
from pygame import K_0, K_2, K_3, K_4, K_5, K_6, K_8, K_9
from backend.eventhandler import EventHandler
from backend.event_functions import select_many
# from backend.levenshtein import probar_input
from frontend import Renderer, WidgetHandler
from .basewidget import BaseWidget


class Entry(BaseWidget):
    f = None
    color_fondo = 255, 255, 255
    color_texto = 0, 0, 0
    lenght = 0
    ticks = 0
    active = True

    status_precio = True
    status_isbn = False

    def __init__(self, x, y):
        self.f = font.SysFont('Verdana', 16)
        self.empty_f = font.SysFont('Verdana', 16, italic=True)
        self.w, self.h = 310, 23
        self.image = Surface((self.w, self.h))
        self.image.fill(self.color_fondo, (1, 1, self.w - 2, self.h - 2))
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__()
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)
        EventHandler.register(self.update_status, 'check')

        self.input = []

    def update_status(self, event):
        name = event.data['name']
        status = event.data['status']
        if name == 'precio':
            self.status_precio = status
        elif name == 'isbn':
            self.status_isbn = status

    def button_trigger(self):
        nombre = ''.join(self.input).upper()
        selection = []
        columns = []
        if self.status_precio:
            columns.append('precio')
        if self.status_isbn:
            columns.append('ISBN')
        selection.extend(select_many(nombre, 'nombre', columns))

        string = ''
        for item in selection:
            string += item['nombre']+':'
            if self.status_precio:
                string += ' Precio: $'+str(item['precio'])
            if self.status_isbn:
                string += ' ISBN: '+item.get('ISBN','-')
            string += '\n'

        EventHandler.trigger('show_text', 'input', {'label': 'precio', 'text': string})

    def on_keydown(self, tecla):
        mods = key.get_mods()
        shift = mods & K_LSHIFT or mods & K_RSHIFT or mods & KMOD_CAPS
        name = key.name(tecla).strip('[]')
        if name == 'space':
            self.input_character(' ')
        elif name == 'backspace':
            self.del_character()
        elif name == 'enter' or name == 'return':
            self.button_trigger()
        elif tecla in (K_LSHIFT, K_RSHIFT):
            pass
        elif name.isdecimal():
            if shift:
                if tecla == K_0:
                    name = '='
                elif tecla == K_2:
                    name = '"'
                elif tecla == K_3:
                    name = '#'
                elif tecla == K_4:
                    name = '$'
                elif tecla == K_5:
                    name = '%'
                elif tecla == K_6:
                    name = '&'
                elif tecla == K_8:
                    name = '('
                elif tecla == K_9:
                    name = ')'
            self.input_character(name)
        elif name.isalpha:
            if shift:
                name = name.upper()
            self.input_character(name)

    def on_mousebuttondown(self, button):
        if button == 1:
            self.active = True

    def input_character(self, char):
        self.input.append(char)
        self.lenght += 1

    def del_character(self):
        if self.lenght > 0:
            del self.input[-1]
            self.lenght -= 1

    def update(self):
        self.ticks += 1
        self.image.fill(self.color_fondo, (1, 1, self.w - 2, self.h - 2))
        if len(self.input):
            t = ''.join(self.input)
            color = self.color_texto
            fuente = self.f
        else:
            t = 'Ingrese el nombre de un producto'
            color = 125, 125, 125
            fuente = self.empty_f

        r = fuente.render(t, 1, color, self.color_fondo)
        rr = r.get_rect(topleft=(self.rect.x + 1, self.rect.y + 1))

        if self.rect.contains(rr):
            self.image.blit(r, (1, 1))
            self.dirty = 1

        if 10 < self.ticks < 30 and len(self.input) and self.active:
            draw.aaline(self.image, self.color_texto, (rr.right-self.rect.x + 2, 3), (rr.right-80 + 2, self.h - 3))
        elif self.ticks > 40:
            self.ticks = 0
