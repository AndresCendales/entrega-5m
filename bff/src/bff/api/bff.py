from drivers.seedwork.presentacion import api
import json
from drivers.seedwork.dominio.excepciones import ExcepcionDominio

from flask import request, session
from flask import Response
from drivers.modulos.drivers.aplicacion.mapeadores import MapeadorRutaDTOJson
from drivers.seedwork.aplicacion.comandos import ejecutar_commando
from drivers.modulos.drivers.aplicacion.comandos.asignar_ruta import AsignarRuta

bp = api.crear_blueprint('drivers', '/drivers')


@bp.route('/rutas', methods=('POST',))
def asignar_ruta_comando():
    try:
        # NOTE Asignamos el valor 'pulsar' para usar la Unidad de trabajo de Pulsar y 
        # no la defecto de SQLAlchemy
        session['uow_metodo'] = 'pulsar'

        ruta_dict = request.json

        map_ruta = MapeadorRutaDTOJson()
        ruta_dto = map_ruta.externo_a_dto(ruta_dict)

        comando = AsignarRuta(ruta=ruta_dto)

        ejecutar_commando(comando)

        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')