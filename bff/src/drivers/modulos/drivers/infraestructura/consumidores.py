import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback

from drivers.modulos.drivers.infraestructura.schema.v1.eventos import EventoRutaAsignada
from drivers.modulos.drivers.infraestructura.schema.v1.comandos import ComandoAsignarDriver


from drivers.modulos.drivers.infraestructura.proyecciones import ProyeccionAsignacionesLista
from drivers.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from drivers.seedwork.infraestructura import utils


def suscribirse_a_eventos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            'eventos-rutas',
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='bff-sub-eventos',
            schema=AvroSchema(EventoRutaAsignada)
        )

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            ejecutar_proyeccion(
                ProyeccionAsignacionesLista(
                    datos.ruta_id,
                    datos.driver_id,
                    datos.estado,
                    datos.fecha_creacion,
                    datos.fecha_creacion
                ),
                app=app
            )
            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos(app=None):
    # return
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe(
            topic='comandos-reserva',
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name='bff-sub-comandos',
            schema=AvroSchema(ComandoAsignarDriver)
        )

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except Exception as e:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()