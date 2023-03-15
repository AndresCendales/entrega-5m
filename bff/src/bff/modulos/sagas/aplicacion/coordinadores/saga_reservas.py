import sys

sys.path.append('..')
from bff.src.bff.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from bff.src.bff.seedwork.dominio.eventos import EventoDominio

# from bff.src.bff.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
# from bff.src.bff.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
# from bff.src.bff.modulos.rutas.aplicacion.comandos.programar_ruta import ProgramarRuta
# from bff.src.bff.modulos.rutas.infraestructura.schema.v1.eventos import EventoRutaProgramada
# from bff.src.bff.modulos.drivers.aplicacion.comandos.crear_reserva import AsignarRuta
# from bff.src.bff.modulos.drivers.infraestructura.schema.v1.eventos import EventoRutaAsignada


class CoordinadorOrdenes(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(
                index=1,
                # comando=CrearOrden,
                # evento=EventoOrdenCreada,
                error=None,
                compensacion=None
            ),
            Transaccion(
                index=2,
                # comando=ProgramarRuta,
                # evento=EventoRutaProgramada,
                error=None,
                compensacion=None
            ),
            Transaccion(
                index=3,
                # comando=AsignarRuta,
                # evento=EventoRutaAsignada,
                error=None,
                compensacion=None
            ),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])

    def terminar(self):
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        print('persistiendo', mensaje)
        # TODO Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # if isinstance(evento, EventoOrdenCreada):
        #     return ProgramarRuta(
        #         fecha_creacion=evento.fecha_creacion,
        #         fecha_actualizacion=evento.fecha_actualizacion,
        #         id=evento.id,
        #         ordenes=[],
        #     )
        return {}
        # raise NotImplementedError("El evento no es soportado por el coordinador")
        # TODO Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        ...


# TODO Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorOrdenes()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")
