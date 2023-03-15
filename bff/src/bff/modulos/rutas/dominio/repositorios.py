""" Interfaces para los repositorios del dominio de vuelos

En este archivo usted encontrará las diferentes interfaces para repositorios
del dominio de vuelos

"""

from abc import ABC
from bff.src.bff.seedwork.dominio.repositorios import Repositorio

class RepositorioRutas(Repositorio, ABC):
    ...

class RepositorioEventosRutas(Repositorio, ABC):
    ...
