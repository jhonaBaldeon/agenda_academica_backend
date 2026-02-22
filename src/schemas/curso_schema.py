from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CursoBase(BaseModel):
    nombre_curso: str = Field(..., validation_alias="nombreCurso")
    nombre_docente: str = Field(..., validation_alias="nombreDocente")
    horario: str
    color: int
    docente_id: str


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    nombre_curso: Optional[str] = Field(None, validation_alias="nombreCurso")
    nombre_docente: Optional[str] = Field(None, validation_alias="nombreDocente")
    horario: Optional[str] = None
    color: Optional[int] = None


class Curso(CursoBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
