from rutas.modulos.rutas.dominio.eventos import RutaProgramada
from rutas.seedwork.aplicacion.handlers import Handler
from rutas.modulos.rutas.infraestructura.despachadores import Despachador

class HandlerRutaIntegracion(Handler):

    @staticmethod
    def handle_ruta_programada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-ruta')
