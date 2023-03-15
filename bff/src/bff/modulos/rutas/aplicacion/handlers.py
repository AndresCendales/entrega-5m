from bff.src.bff.modulos.rutas.dominio.eventos import RutaProgramada
from bff.src.bff.seedwork.aplicacion.handlers import Handler
from bff.src.bff.modulos.rutas.infraestructura.despachadores import Despachador

class HandlerRutaIntegracion(Handler):

    @staticmethod
    def handle_ruta_programada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ruta')
