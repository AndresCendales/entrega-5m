from ordenes.modulos.ordenes.dominio.eventos import OrdenCreada
from ordenes.seedwork.aplicacion.handlers import Handler
from ordenes.modulos.ordenes.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, 'eventos-orden')
