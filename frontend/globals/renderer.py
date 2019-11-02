from pygame import display, init, image, draw, error
from pygame.sprite import LayeredUpdates
from .constantes import ALTO, ANCHO, COLOR_FONDO
import os


class Renderer:
    contents = None

    @classmethod
    def init(cls):
        init()
        os.environ['SDL_VIDEO_CENTERED'] = "{!s},{!s}".format(0, 0)
        try:
            icon = image.load(os.path.join(os.getcwd(), 'lib', 'frontend', 'icon.png'))
        except error:
            icon = image.load(os.path.join(os.getcwd(), 'frontend', 'icon.png'))
        icon.set_colorkey((255, 255, 255, 0))
        display.set_icon(icon)
        display.set_caption("PMCDB: PyMavisCustomDatabase v0.2.2")
        display.set_mode((ANCHO, ALTO))
        cls.contents = LayeredUpdates()

    @classmethod
    def add_widget(cls, widget, layer=1):
        cls.contents.add(widget, layer=layer)

    @classmethod
    def del_widget(cls, widget):
        cls.contents.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        fondo.fill(COLOR_FONDO)
        cls.contents.draw(fondo)
        draw.line(fondo, [0, 0, 0], [640, 0], [640, ALTO], 1)
        display.flip()


Renderer.init()
