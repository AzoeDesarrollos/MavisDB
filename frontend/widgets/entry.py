from pygame import Surface, font, key, draw, K_LSHIFT, K_RSHIFT, KMOD_CAPS
from pygame import K_0, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9
from backend.eventhandler import EventHandler
from backend.database import select_many
# from backend.levenshtein import probar_input
from frontend import Renderer, WidgetHandler
from .basewidget import BaseWidget


class Entry(BaseWidget):
    f = None
    color_fondo = 255, 255, 255
    color_texto = 0, 0, 0
    lenght = 0
    ticks = 0

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
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)
        WidgetHandler.set_active(self)
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
        columns = []
        if self.status_precio:
            columns.append('precio')
        if self.status_isbn:
            columns.append('ISBN')
        selection = select_many(nombre, 'nombre', columns) if len(self.input) > 0 else []
        EventHandler.trigger('show_text', 'input', {'text': selection})

    def on_keydown(self, tecla):
        mods = key.get_mods()
        shift = mods & K_LSHIFT or mods & K_RSHIFT or mods & KMOD_CAPS
        name = key.name(tecla).strip('[]')
        self.activate()
        if name == 'space':
            self.input_character(' ')
        elif name == 'backspace':
            self.del_character()
        elif name == 'enter' or name == 'return':
            self.button_trigger()
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
                elif tecla == K_7:
                    name = '•'
                elif tecla == K_8:
                    name = '('
                elif tecla == K_9:
                    name = ')'
            self.input_character(name)
        elif name.isalpha and len(name) == 1:
            if shift:
                if name == '.':
                    name = ':'
                if name == ',':
                    name = ';'
                name = name.upper()
            self.input_character(name)

    def on_mousebuttondown(self, button):
        if button == 1:
            self.activate()

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
        elif not self.active:
            t = 'Ingrese el nombre de un producto'
            color = 125, 125, 125
            fuente = self.empty_f
        else:
            t = ''
            color = self.color_texto
            fuente = self.f

        r = fuente.render(t, 1, color, self.color_fondo)
        rr = r.get_rect(topleft=(self.rect.x + 1, self.rect.y + 1))

        if self.rect.contains(rr):
            self.image.blit(r, (1, 1))

        if 10 < self.ticks < 30 and self.active:
            draw.aaline(self.image, self.color_texto, (rr.right - self.rect.x + 2, 3), (rr.right - 80 + 2, self.h - 3))
        elif self.ticks > 40:
            self.ticks = 0
