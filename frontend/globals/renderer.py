from pygame import display, init
from pygame.sprite import LayeredDirty
from .constantes import ALTO, ANCHO, COLOR_FONDO
import os


class Renderer:
    contents = None

    @classmethod
    def init(cls):
        init()
        os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)
        display.set_caption("PyMavisDatabase")
        display.set_mode((ANCHO, ALTO))
        cls.contents = LayeredDirty()

    @classmethod
    def add_widget(cls, widget, layer):
        cls.contents.add(widget, layer=layer)

    @classmethod
    def del_widget(cls, widget):
        cls.contents.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        fondo.fill(COLOR_FONDO)
        rect = cls.contents.draw(fondo)
        display.update(rect)


Renderer.init()
