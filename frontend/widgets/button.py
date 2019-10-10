from pygame import Surface, font
from .basewidget import BaseWidget
from frontend import Renderer, WidgetHandler


class Button(BaseWidget):
    action = None

    def __init__(self, x, y, texto, action=None):
        self.f = font.SysFont('Verdana', 16)
        self.img_unp = self.crear(texto, (0, 0, 0))
        self.img_pre = self.crear(texto, (255, 255, 255))
        self.image = self.img_unp
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__()
        Renderer.add_widget(self, 1)
        WidgetHandler.add_widget(self, 1)
        self.action = action

    def crear(self, texto, color_texto):
        w, h = self.f.size(texto)
        image = Surface((w + 4, h + 2))
        image.fill((125, 125, 125), (1, 1, w + 2, h))
        render = self.f.render(texto, 1, color_texto, (125, 125, 125))
        image.blit(render, (2, 1))
        return image

    def on_mousebuttondown(self, button):
        if button == 1 and self.action is not None:
            self.image = self.img_pre
            self.action()

    def on_mousebuttonup(self, button):
        if button == 1:
            self.image = self.img_unp

    def on_mouseover(self):
        pass

    def update(self):
        self.dirty = 1
