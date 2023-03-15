from drivers.seedwork.aplicacion.queries import QueryHandler
from drivers.modulos.drivers.infraestructura.fabricas import FabricaVista
from drivers.modulos.drivers.dominio.fabricas import FabricaRutas

class ReservaQueryBaseHandler(QueryHandler):
    def __init__(self):
        self._fabrica_vista: FabricaVista = FabricaVista()
        self._fabrica_vuelos: FabricaRutas = FabricaRutas()

    @property
    def fabrica_vista(self):
        return self._fabrica_vista
    
    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos    