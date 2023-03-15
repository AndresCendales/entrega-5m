import sys

sys.path.append('..')
from bff.src.bff.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from bff.src.bff.seedwork.dominio.eventos import EventoDominio

from bff.src.bff.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from bff.src.bff.modulos.ordenes.aplicacion.comandos.cancelar_orden import CancelarOrden
from bff.src.bff.modulos.ordenes.dominio.eventos import OrdenCreada,OrdenCreadaFallida

from bff.src.bff.modulos.rutas.aplicacion.comandos.programar_ruta import ProgramarRuta
#from bff.src.bff.modulos.rutas.aplicacion.comandos.cancelar_ruta import CancelarRuta
from bff.src.bff.modulos.rutas.dominio.eventos import RutaProgramada,RutaProgramadaFallida

from bff.src.bff.modulos.drivers.aplicacion.comandos.crear_asignacion import AsignarRuta as AsignarDriver
from bff.src.bff.modulos.drivers.aplicacion.comandos.cancelar_asignacion import CancelarAsignacion
from bff.src.bff.modulos.drivers.dominio.eventos import RutaAsignada,RutaAsignadaFallida


class CoordinadorOrdenes(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(
                index=1,
                comando=CrearOrden, 
                evento=OrdenCreada,
                error=OrdenCreadaFallida,
                compensacion=CancelarOrden,
                exitosa=True
            ),
            Transaccion(
                index=2,
                comando=ProgramarRuta, #
                evento=RutaProgramada,#
                error=RutaProgramadaFallida,
                compensacion=None,
                exitosa=True
            ),
            Transaccion(
                index=3,
                comando=AsignarDriver,
                evento=RutaAsignada,#
                error=RutaAsignadaFallida,
                compensacion=CancelarAsignacion,
                exitosa=True
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
        if isinstance(evento, OrdenCreada):
            return ProgramarRuta(
                fecha_creacion=evento.fecha_creacion,
                fecha_actualizacion=evento.fecha_creacion,
                id=evento.id,
                ordenes=[],
            )

        print('-'*10)
        print(type(evento).__name__)
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
        coordinador.inicializar_pasos()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")
