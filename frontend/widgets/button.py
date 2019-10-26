from pygame import Surface, font
from .basewidget import BaseWidget
from frontend import Renderer, WidgetHandler


class Button(BaseWidget):
    action = None

    def __init__(self, x, y, texto, action=None, font_size=16):
        self.f = font.SysFont('Verdana', font_size)
        self.img_unp = self.crear(texto, (0, 0, 0))
        self.img_pre = self.crear(texto, (255, 255, 255))
        self.image = self.img_unp
        self.rect = self.image.get_rect(topleft=(x, y))
        super().__init__()
        WidgetHandler.add_widget(self)
        self.show()
        self.action = action

    def crear(self, texto, color_texto):
        w, h = self.f.size(texto)
        image = Surface((w + 4, h + 2))
        image.fill((125, 125, 125), (1, 1, w + 2, h))
        render = self.f.render(texto, 1, color_texto, (125, 125, 125))
        image.blit(render, (2, 1))
        return image

    def on_mousebuttondown(self, button):
        if button == 1:
            self.image = self.img_pre
            self.action() if self.action is not None else None

    def on_mousebuttonup(self, button):
        if button == 1:
            self.image = self.img_unp

    def show(self):
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def hide(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def on_mouseover(self):
        pass

    def update(self):
        self.dirty = 1
