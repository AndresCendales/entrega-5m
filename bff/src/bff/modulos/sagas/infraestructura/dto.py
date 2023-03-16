"""DTOs para la capa de infrastructura del dominio de drivers

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de drivers

"""
from __future__ import annotations
from bff.src.config.db import db
from sqlalchemy.orm import declarative_base, relationship

import uuid

Base = db.declarative_base()

class Eventos(db.Model):
    __tablename__ = "eventos"
    __table_args__ = {"schema": "family_2"}
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    evento = db.Column(db.String(200), nullable=False)
