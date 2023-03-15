from pulsar.schema import *
from bff.src.bff.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoAsignarDriverPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Cree los records para itinerarios

class ComandoAsignarDriver(ComandoIntegracion):
    data = ComandoAsignarDriverPayload()