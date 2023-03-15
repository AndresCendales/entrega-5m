from rutas.seedwork.infraestructura.proyecciones import Proyeccion, ProyeccionHandler
from rutas.seedwork.infraestructura.proyecciones import ejecutar_proyeccion as proyeccion
from rutas.modulos.rutas.infraestructura.fabricas import FabricaRepositorio
from rutas.modulos.rutas.infraestructura.repositorios import RepositorioRutas
from rutas.modulos.rutas.dominio.entidades import Ruta
from rutas.modulos.rutas.infraestructura.dto import Ruta as RutaDTO

from rutas.seedwork.infraestructura.utils import millis_a_datetime
import datetime
import logging
import traceback
from abc import ABC, abstractmethod

class ProyeccionRuta(Proyeccion, ABC):
    @abstractmethod
    def ejecutar(self):
        ...

class ProyeccionRutasLista(ProyeccionRuta):
    def __init__(self, id_ruta):
        self.id_ruta = id_ruta
    
    def ejecutar(self, db=None):
        if not db:
            logging.error('ERROR: DB del app no puede ser nula')
            return
        
        fabrica_repositorio = FabricaRepositorio()
        repositorio = fabrica_repositorio.crear_objeto(RepositorioRutas)
        
        repositorio.agregar(
            Ruta(id=str(self.id_ruta)))
        
        db.session.commit()

class ProyeccionRutaHandler(ProyeccionHandler):
    
    def handle(self, proyeccion: ProyeccionRuta):
        from rutas.config.db import db
        proyeccion.ejecutar(db=db)
        

@proyeccion.register(ProyeccionRutasLista)
def ejecutar_proyeccion_ruta(proyeccion, app=None):
    if not app:
        logging.error('ERROR: Contexto del app no puede ser nulo')
        return
    try:
        with app.app_context():
            handler = ProyeccionRutaHandler()
            handler.handle(proyeccion)
            
    except:
        traceback.print_exc()
        logging.error('ERROR: Persistiendo!')
    