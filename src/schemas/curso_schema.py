from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CursoBase(BaseModel):
    nombre_curso: str
    nombre_docente: str
    horario: str
    color: int
    docente_id: str


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nombre_curso: Optional[str] = None
    nombre_docente: Optional[str] = None
    horario: Optional[str] = None
    color: Optional[int] = None
    docente_id: Optional[str] = None


class Curso(CursoBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
