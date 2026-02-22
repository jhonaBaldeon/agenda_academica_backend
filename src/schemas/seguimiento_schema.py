from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class EstadoSeguimiento(str, Enum):
    completado = "completado"
    incompleto = "incompleto"
    no_realizado = "noRealizado"


class PrioridadActividad(str, Enum):
    alta = "alta"
    media = "media"
    baja = "baja"


class SeguimientoBase(BaseModel):
    alumno_id: str
    alumno_nombre: str
    actividad_id: str
    actividad_titulo: str
    actividad_descripcion: str
    actividad_fecha_entrega: datetime
    actividad_prioridad: PrioridadActividad = PrioridadActividad.media
    curso_id: str
    curso_nombre: str
    estado: EstadoSeguimiento = EstadoSeguimiento.incompleto
    observaciones: Optional[str] = None


class SeguimientoCreate(SeguimientoBase):
    pass


class SeguimientoUpdate(BaseModel):
    estado: Optional[EstadoSeguimiento] = None
    observaciones: Optional[str] = None
    actividad_titulo: Optional[str] = None
    actividad_descripcion: Optional[str] = None
    actividad_fecha_entrega: Optional[datetime] = None
    actividad_prioridad: Optional[PrioridadActividad] = None
    curso_nombre: Optional[str] = None


class Seguimiento(SeguimientoBase):
    id: str
    fecha_completado: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
