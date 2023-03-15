from drivers.seedwork.presentacion import api
import json
from drivers.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from drivers.modulos.drivers.aplicacion.mapeadores import MapeadorRutaDTOJson
from drivers.seedwork.aplicacion.comandos import ejecutar_commando
from drivers.modulos.drivers.aplicacion.comandos.asignar_ruta import AsignarRuta

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

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')