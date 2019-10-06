from frontend import Renderer, WidgetHandler, COLOR_FONDO, COLOR_TEXTO
from frontend.globals.textrect import render_textrect
from backend.eventhandler import EventHandler
from .basewidget import BaseWidget
from pygame import font, Rect, K_DOWN, K_UP, Surface


class Label(BaseWidget):
    render = None
    scroll_y = 0

    def __init__(self, name, text, x, y):
        self.x, self.y = x, y
        self.name = name
        rect = Rect(self.x, self.y, 640, 480 - y)
        self.w, self.h = rect.size
        self.f = font.SysFont('Verdana', 16)
        self.text = text
        EventHandler.register(self.show, 'show_text')
        super().__init__(Surface(rect.size), rect)
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
