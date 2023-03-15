from pulsar.schema import *
from dataclasses import dataclass, field
from bff.src.bff.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoProgramarRutaPayload(ComandoIntegracion):
    id = String()

class ComandoProgramarRuta(ComandoIntegracion):
    data = ComandoProgramarRutaPayload()