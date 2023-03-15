"""Entidades del dominio de ordenes

En este archivo usted encontrará las entidades del dominio de ordenes

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import ordenes.modulos.ordenes.dominio.objetos_valor as ov
from ordenes.modulos.ordenes.dominio.eventos import OrdenCreada
from ordenes.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Producto(Entidad):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)

@dataclass
class Orden(AgregacionRaiz):
    client_id: str= field(default_factory=str)
    origen: ov.Ubicacion= field(default_factory=ov.Ubicacion)
    destino: ov.Ubicacion= field(default_factory=ov.Ubicacion)
    tipo: str = field(default_factory=str)
    productos: list[Producto] = field(default_factory=list[Producto])

    def crear_orden(self, orden: Orden):
        self.client_id = orden.client_id
        self.origen = orden.origen
        self.destino = orden.destino
        self.tipo = orden.tipo
        self.productos = orden.productos
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(OrdenCreada(id_orden=self.id, id_cliente=self.client_id, tipo=self.tipo, 
                                        productos=self.productos, fecha_creacion=self.fecha_creacion))
