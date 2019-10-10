from frontend import Renderer, WidgetHandler, COLOR_FONDO, COLOR_TEXTO
from frontend.globals.textrect import render_textrect
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from pygame import font, Rect, K_DOWN, K_UP, Surface


class Label(BaseWidget):
    render = None
    scroll_y = 0

    def __init__(self, name, text, x, y, w, h=0, size=16):
        self.x, self.y = x, y
        self.text = text
        self.name = name
        self.f = font.SysFont('Verdana', size)
        if self.text != '':
            self.render = render_textrect(self.text, self.f, w, COLOR_TEXTO, COLOR_FONDO)
            self.w, self.h = self.render.get_size()
            self.rect = self.render.get_rect(topleft=(x, y))
            self.image = Surface(self.rect.size)
            self.image.blit(self.render, (0, self.scroll_y))
        else:
            self.w, self.h = w, h
            self.image = Surface((self.w, self.h))
            self.rect = Rect(self.x, self.y, self.w, self.h)

        EventHandler.register(self.show, 'show_text')
        super().__init__()
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)

    def show(self, event):
        if event.data['label'] == self.name:
            self.text = event.data.get('text')

    def on_keydown(self, key):
        if key == K_DOWN:
            self.scroll(-21)
        elif key == K_UP:
            self.scroll(+21)

    def on_mousebuttondown(self, button):
        if button == 5:  # down
            self.scroll(-21)
        elif button == 4:  # up
            self.scroll(+21)

    def scroll(self, direction):
        w, h = self.render.get_size()
        if all([h-self.h+self.scroll_y+direction > -3, self.scroll_y+direction <= 0]):
            self.scroll_y += direction

    def update(self):
        self.image.fill(COLOR_FONDO)
        self.render = render_textrect(self.text, self.f, self.w, COLOR_TEXTO, COLOR_FONDO)
        self.image.blit(self.render, (0, self.scroll_y))
        self.dirty = 1
