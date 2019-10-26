from pygame import Surface, draw
from .basewidget import BaseWidget
from frontend import Renderer, WidgetHandler
from backend.eventhandler import EventHandler


class Checkbox(BaseWidget):
    state = None

    def __init__(self, x, y, name, initial_state=False):
        super().__init__()
        self.x, self.y = x, y
        self.nombre = name
        self.img_true = self._crear(True)
        self.img_false = self._crear(False)
        self.state = initial_state
        if self.state:
            self.image = self.img_true
        else:
            self.image = self.img_false
        self.rect = self.image.get_rect(center=(self.x, self.y))

        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)
        EventHandler.trigger('check', self, {'name': self.nombre, 'status': self.state})

    @staticmethod
    def _crear(checked):
        lado = 12
        img = Surface((lado, lado))
        img.fill((255, 255, 255), (1, 1, lado - 2, lado - 2))

        if checked:
            draw.aaline(img, (0, 0, 0), [2, 2], [9, 10])  # \
            draw.aaline(img, (0, 0, 0), [2, 10], [9, 2])  # /

        return img

    def check(self):
        self.state = not self.state
        if self.state:
            self.image = self.img_true
        else:
            self.image = self.img_false

        EventHandler.trigger('check', self, {'name': self.nombre, 'status': self.state})

    def on_mousebuttondown(self, button):
        self.check()