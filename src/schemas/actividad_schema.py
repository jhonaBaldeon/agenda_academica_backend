from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class PrioridadActividad(str, Enum):
    alta = "alta"
    media = "media"
    baja = "baja"


class EstadoActividad(str, Enum):
    completado = "completado"
    incompleto = "incompleto"
    no_realizado = "noRealizado"


class ActividadBase(BaseModel):
    curso_id: str
    titulo: str
    descripcion: str
    fecha_entrega: datetime
    prioridad: PrioridadActividad = PrioridadActividad.media


class ActividadCreate(ActividadBase):
    pass


class ActividadUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_entrega: Optional[datetime] = None
    prioridad: Optional[PrioridadActividad] = None
    estado: Optional[EstadoActividad] = None


class Actividad(ActividadBase):
    id: str
    estado: EstadoActividad = EstadoActividad.incompleto
    created_at: datetime

    class Config:
        from_attributes = True
