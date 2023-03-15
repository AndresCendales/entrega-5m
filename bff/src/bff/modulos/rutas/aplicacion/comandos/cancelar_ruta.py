from bff.src.bff.seedwork.aplicacion.comandos import Comando
from bff.src.bff.modulos.rutas.aplicacion.dto import OrdenDTO, RutaDTO
from .base import ProgramarRutaBaseHandler
from dataclasses import dataclass
from bff.src.bff.seedwork.aplicacion.comandos import ejecutar_commando as comando

from bff.src.bff.modulos.rutas.dominio.entidades import Ruta
from bff.src.bff.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from bff.src.bff.modulos.rutas.aplicacion.mapeadores import MapeadorRuta
from bff.src.bff.modulos.rutas.infraestructura.repositorios import RepositorioRutas, RepositorioEventosRutas

@dataclass
class CancelarRuta(Comando):
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    ordenes: list[OrdenDTO]

class CancelarRutaHandler(CancelarRutaBaseHandler):
    
    def handle(self, comando: CancelarRuta):
        ruta_dto = RutaDTO(
                fecha_actualizacion=comando.fecha_actualizacion
            ,   fecha_creacion=comando.fecha_creacion
            ,   id=comando.id
            ,   ordenes=comando.ordenes)

        ruta: Ruta = self.fabrica_rutas.crear_objeto(ruta_dto, MapeadorRuta())
        ruta.programar_ruta(ruta)

        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioRutas)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosRutas)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, ruta, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()


@comando.register(CancelarRuta)
def ejecutar_comando_programar_ruta(comando: CancelarRuta):
    handler = CancelarRutaHandler()
    handler.handle(comando)
    