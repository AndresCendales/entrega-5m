import sys 
sys.path.append('..')

import pulsar, _pulsar
from pulsar.schema import *
from ordenes.src.alpesonline.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
import logging
import traceback


def suscribirse_a_eventos(topico, suscripcion):
    cliente = None
    try:
        cliente = pulsar.Client('pulsar://127.0.0.1:6650')
        consumidor = cliente.subscribe(
            topico,
            consumer_type=_pulsar.ConsumerType.Shared,
            subscription_name=suscripcion,
            schema=AvroSchema(EventoOrdenCreada)
        )

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento recibido: {datos}')

            # ejecutar_proyeccion(ProyeccionRutasLista(datos.id_ruta), app=app)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except Exception as e:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()


if __name__ == '__main__':
    suscribirse_a_eventos('eventos-orden', 'ordenes-sub-eventos-test')
