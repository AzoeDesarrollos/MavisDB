from frontend.widgets import *


class AreaBusqueda:
    @classmethod
    def init(cls):
        Label('Producto:', 0, 10, w=80)
        e = Entry(80, 10)
        b = Button(e.rect.right + 10, 10, 'Consulta', e.button_trigger)
        CartableLabelList(0, 40, w=600)
        p = Label('Precio:', b.rect.right + 10, e.rect.top+3, w=43, size=12)
        i = Label('ISBN:', p.rect.right + 30, e.rect.top+3, w=43, size=12)
        Checkbox(p.rect.right + 10, p.rect.centery, 'precio', initial_state=True)
        Checkbox(i.rect.right + 5, i.rect.centery, 'isbn')
