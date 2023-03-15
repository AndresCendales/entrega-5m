""" Interfaces para los repositorios del dominio de ordenes

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de ordenes

"""

from abc import ABC
from bff.src.bff.seedwork.dominio.repositorios import Repositorio

class RepositorioOrdenes(Repositorio, ABC):
    ...

class RepositorioEventosOrdenes(Repositorio, ABC):
    ...
