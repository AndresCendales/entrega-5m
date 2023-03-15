""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de rutas

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos en la capa de infraestructura del dominio de rutas

"""

from dataclasses import dataclass, field
from bff.src.bff.seedwork.dominio.fabricas import Fabrica
from bff.src.bff.seedwork.dominio.repositorios import Repositorio
from bff.src.bff.seedwork.infraestructura.vistas import Vista
from bff.src.bff.modulos.ordenes.dominio.entidades import Orden
from bff.src.bff.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes
from .repositorios import RepositorioOrdenesSQLAlchemy, RepositorioEventosOrdenSQLAlchemy
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioOrdenes:
            return RepositorioOrdenesSQLAlchemy()
        elif obj == RepositorioEventosOrdenes:
            return RepositorioEventosOrdenSQLAlchemy()
        else:
            raise ExcepcionFabrica(f'No existe fábrica para el objeto {obj}')
