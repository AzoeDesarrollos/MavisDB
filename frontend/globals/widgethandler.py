from pygame import event, QUIT, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import K_ESCAPE, time, mouse
from backend.eventhandler import EventHandler
from pygame.sprite import LayeredUpdates


class WidgetHandler:
    contents = None
    active = None
    clock = None

    @classmethod
    def init(cls):
        cls.contents = LayeredUpdates()
        cls.clock = time.Clock()

    @classmethod
    def add_widget(cls, widget, layer=1):
        cls.contents.add(widget, layer=layer)

    @classmethod
    def del_widget(cls, widget):
        cls.contents.remove(widget)

    @classmethod
    def set_active(cls, widget):
        for wdg in cls.contents:
            wdg.deactivate()
        # no se activa al widget per se adrede.
        # de esta manera Entry se comporta como debería.
        cls.active = widget

    @classmethod
    def update(cls):
        cls.clock.tick(60)
        events = event.get([KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT])
        event.clear()
        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                EventHandler.trigger('salir', 'engine', {'mensaje': 'normal'})

            elif e.type == KEYDOWN:
                if cls.active is not None:
                    cls.active.on_keydown(e.key)

            elif e.type == MOUSEBUTTONDOWN:
                for wig in cls.contents:
                    wig.deactivate()
                widgets = [i for i in cls.contents.sprites() if i.rect.collidepoint(e.pos)]
                for w in widgets:
                    w.on_mousebuttondown(e.button)
                    cls.active = w

            elif e.type == MOUSEBUTTONUP:
                widgets = [i for i in cls.contents.sprites() if i.rect.collidepoint(e.pos)]
                for w in widgets:
                    w.on_mousebuttonup(e.button)

        x, y = mouse.get_pos()
        for widget in cls.contents.sprites():
            if widget.rect.collidepoint((x, y)):
                widget.on_mouseover()

        cls.contents.update()


WidgetHandler.init()
