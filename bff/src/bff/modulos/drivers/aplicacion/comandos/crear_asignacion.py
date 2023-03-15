from bff.src.bff.seedwork.aplicacion.comandos import Comando
from bff.src.bff.modulos.drivers.aplicacion.dto import RutaDTO
from .base import AsignarRutaBaseHandler
from dataclasses import dataclass
from bff.src.bff.seedwork.aplicacion.comandos import ejecutar_commando as comando

from bff.src.bff.modulos.drivers.dominio.entidades import Ruta
from bff.src.bff.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from bff.src.bff.modulos.drivers.aplicacion.mapeadores import MapeadorRuta
from bff.src.bff.modulos.drivers.infraestructura.repositorios import RepositorioRutas, RepositorioEventosRutas

@dataclass
class AsignarRuta(Comando):
    ruta: RutaDTO


class AsignarRutaHandler(AsignarRutaBaseHandler):
    
    def handle(self, comando: AsignarRuta):
        ruta: Ruta = self.fabrica_rutas.crear_objeto(comando.ruta, MapeadorRuta())
        ruta.asignar_ruta(ruta)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRutas)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosRutas)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, ruta, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(AsignarRuta)
def ejecutar_comando_crear_reserva(comando: AsignarRuta):
    handler = AsignarRutaHandler()
    handler.handle(comando)
    