import pulsar
from pulsar.schema import *
from bff.src.bff.seedwork.infraestructura import utils
import requests
import json
from fastavro.schema import parse_schema
def publicar_mensaje(mensaje, topico, schema):
        json_schema = consultar_schema_registry(schema)  
        avro_schema = obtener_schema_avro_de_diccionario(json_schema)

        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=avro_schema)
        publicador.send(mensaje)
        cliente.close()

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{utils.broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)
