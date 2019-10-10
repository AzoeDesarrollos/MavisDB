from frontend import Renderer, WidgetHandler, ANCHO
from backend import EventHandler
from frontend.widgets import *

Label('etq', 'Producto:', 0, 50, w=80)
Label('version', "v0.1", ANCHO-40, 0, w=40)
# Button(0, 0, 'Recargar DBs', None)
e = Entry(80, 50)
b = Button(e.rect.right + 10, 50, 'Consulta', e.button_trigger)
Label('precio', '', 0, 100, w=ANCHO, h=380)
p = Label('check_precio', 'Precio:', b.rect.right + 10, e.rect.top+3, w=43, size=12)
i = Label('check_precio', 'ISBN:', p.rect.right + 30, e.rect.top+3, w=43, size=12)
Checkbox(p.rect.right + 10, p.rect.centery, 'precio', initial_state=True)
Checkbox(i.rect.right + 5, i.rect.centery, 'isbn')

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
