from pygame import Surface, font, key, draw, KMOD_SHIFT, KMOD_CAPS
from pygame import K_0, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9
from backend.eventhandler import EventHandler
from backend.database import select_many
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

    acento = False

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
        selection = select_many(nombre, columns) if len(self.input) > 0 else []
        EventHandler.trigger('show_text', 'input', {'text': selection})

    def on_keydown(self, tecla):
        mods = key.get_mods()
        shift = mods & KMOD_SHIFT or mods & KMOD_CAPS
        raw = key.name(tecla).strip('[]')
        name = None
        if raw == 'space':
            self.input_character(' ')
        elif raw == 'backspace':
            self.del_character()
        elif raw in ['enter', 'return']:
            self.button_trigger()
        elif raw.isdecimal():
            if tecla == K_0:
                name = '=' if shift else raw
            elif tecla == K_2:
                name = '"' if shift else raw
            elif tecla == K_3:
                name = '#' if shift else raw
            elif tecla == K_4:
                name = '$' if shift else raw
            elif tecla == K_5:
                name = '%' if shift else raw
            elif tecla == K_6:
                name = '&' if shift else raw
            elif tecla == K_7:
                name = '•' if shift else raw
            elif tecla == K_8:
                name = '(' if shift else raw
            elif tecla == K_9:
                name = ')' if shift else raw
            else:
                name = raw

        elif raw.isalpha and len(raw) == 1:
            if raw == '.':
                name = ':' if shift else raw
            elif raw == ',':
                name = ';' if shift else raw
            elif raw == "´":
                self.acento = True
            elif raw == "'":
                name = "?" if shift else "'"
            elif raw == '¡':
                name = '¿' if shift else '¡'
            else:
                name = raw.upper() if shift else raw

            if self.acento:
                vowels = 'aeiou'
                accented_v = 'áéíóú'
                if raw in vowels:
                    name = accented_v[vowels.index(raw)]
                    name = name.upper() if shift else name

        if name is not None:
            self.acento = False
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
