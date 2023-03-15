import pulsar, _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from bff.src.bff.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
from bff.src.bff.modulos.rutas.infraestructura.schema.v1.eventos import EventoRutaProgramada
from bff.src.bff.modulos.ordenes.dominio.eventos import OrdenCreada
from bff.src.bff.modulos.rutas.dominio.eventos import RutaProgramada
# from alpesonline.modulos.ordenes.infraestructura.schema.v1.comandos import ComandoCrearOrden

# from alpesonline.modulos.ordenes.infraestructura.proyecciones import ProyeccionOrdenesLista
# from alpesonline.seedwork.infraestructura.proyecciones import ejecutar_proyeccion
from bff.src.bff.seedwork.infraestructura import utils
from bff.src.bff.modulos.sagas.aplicacion.coordinadores.saga_reservas import oir_mensaje

def suscribirse_a_eventos_ordenes(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='alpesonline-sub-eventos',
                                       schema=AvroSchema(EventoOrdenCreada)
        )
        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento orden recibido: {datos}')
            oir_mensaje(OrdenCreada(
                id=uuid.uuid4(),
                id_orden=datos.id_orden,
                id_cliente=datos.id_cliente,
                tipo=datos.tipo,
                productos=[],
                fecha_creacion=datetime.datetime.fromtimestamp(datos.fecha_creacion / 1000.0)
            ))
            # TODO: agregar los demas campos para guardar en BD
            # ejecutar_proyeccion(ProyeccionOrdenesLista(datos.id_orden), app=app)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_eventos_ruta(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-ruta', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='bff-sub-eventos-ruta', schema=AvroSchema(EventoRutaProgramada))

        while True:
            mensaje = consumidor.receive()
            datos = mensaje.value().data
            print(f'Evento ruta recibido: {datos}')
            oir_mensaje(RutaProgramada(
                id=uuid.uuid4(),
                id_ruta=datos.id_ruta,
                ordenes=[],
                fecha_creacion=datetime.datetime.now()
            ))            
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()