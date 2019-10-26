from frontend import Renderer, WidgetHandler, AreaBusqueda, AreaVentas
from backend import EventHandler

AreaBusqueda.init()
# AreaVentas.init(900-640)

while True:
    EventHandler.process()
    WidgetHandler.update()
    Renderer.update()
