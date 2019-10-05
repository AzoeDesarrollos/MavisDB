from pygame import event, QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION
from pygame import K_ESCAPE, time, mouse
from backend.eventhandler import EventHandler
from pygame.sprite import LayeredDirty


class WidgetHandler:
    contents = None
    active = None
    clock = None

    @classmethod
    def init(cls):
        cls.contents = LayeredDirty()
        cls.clock = time.Clock()

    @classmethod
    def add_widget(cls, widget, layer):
        cls.contents.add(widget, layer=layer)
        if widget.active:
            cls.active = widget

    @classmethod
    def del_widget(cls, widget):
        cls.contents.remove(widget)

    @classmethod
    def update(cls):
        cls.clock.tick(30)
        events = event.get([KEYDOWN, MOUSEBUTTONDOWN, QUIT])
        event.clear()
        for e in events:
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                EventHandler.trigger('salir', 'engine', {'mensaje': 'normal'})

            elif e.type == KEYDOWN:
                if cls.active is not None:
                    cls.active.on_keydown(e.key)

            elif e.type == KEYUP:
                if cls.active is not None:
                    cls.active.on_keyup(e.key)

            elif e.type == MOUSEBUTTONDOWN:
                for wig in cls.contents:
                    wig.active = False
                widgets = [i for i in cls.contents.sprites() if i.rect.collidepoint(e.pos)]
                for w in widgets:
                    w.on_mousebuttondown(e.button)
                    cls.active = w

            elif e.type == MOUSEBUTTONUP:
                pass

            elif e.tyoe == MOUSEMOTION:
                pass

        x, y = mouse.get_pos()
        for widget in cls.contents.sprites():
            if widget.rect.collidepoint((x, y)):
                widget.on_mouseover()

        cls.contents.update()


WidgetHandler.init()
