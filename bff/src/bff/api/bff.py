from bff.src.bff.seedwork.presentacion import api
import json
from bff.src.bff.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from bff.src.bff.modulos.ordenes.aplicacion.mapeadores import MapeadorOrdenDTOJson
from bff.src.bff.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from bff.src.bff.seedwork.aplicacion.comandos import ejecutar_commando
from bff.src.bff.modulos.utils.publicar import publicar_mensaje
import uuid
from bff.src.bff.seedwork.infraestructura import utils
bp = api.crear_blueprint('ordenes', '/ordenes')


@bp.route('/', methods=('POST',))
def crear_usando_comando():
    try:
        session['uow_metodo'] = 'pulsar'

        orden_dict = request.json

        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)

        comando = CrearOrden(orden_dto.fecha_creacion, orden_dto.fecha_actualizacion, orden_dto.id, orden_dto.client_id,
                             orden_dto.origen, orden_dto.destino, orden_dto.tipo, orden_dto.productos)
        
        # ejecutar_commando(comando)
        publicar_mensaje(
            mensaje=dict(
                id = str(uuid.uuid4()),
                time=utils.time_millis(),
                specversion = "v1",
                type = "ComandoCrearOrden",
                ingestion=utils.time_millis(),
                datacontenttype="AVRO",
                service_name = "BFF Web",
                data = dict(
                    id=orden_dto.client_id
                )
            ),
            topico='comandos-orden',
            schema='public/default/comandos-orden'
        )

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')