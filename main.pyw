from frontend import Renderer, WidgetHandler, AreaBusqueda, AreaVentas
from backend import EventHandler

AreaBusqueda.init()
AreaVentas.init()

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
