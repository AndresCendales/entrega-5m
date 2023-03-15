from bff.src.bff.modulos.ordenes.dominio.eventos import OrdenCreada
from bff.src.bff.seedwork.aplicacion.handlers import Handler
from bff.src.bff.modulos.ordenes.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')
