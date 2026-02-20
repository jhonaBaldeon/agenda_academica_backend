from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlumnoBase(BaseModel):
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    grado: str
    seccion: str
    padre_id: str = ""


class AlumnoCreate(AlumnoBase):
    pass


class AlumnoUpdate(BaseModel):
    nombres: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    grado: Optional[str] = None
    seccion: Optional[str] = None
    padre_id: Optional[str] = None


class Alumno(AlumnoBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
