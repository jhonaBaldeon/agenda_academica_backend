from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CursoBase(BaseModel):
    model_config = {"populate_by_name": True}

    nombre_curso: str = Field(..., alias="nombreCurso")
    nombre_docente: str = Field(..., alias="nombreDocente")
    horario: str
    color: int
    docente_id: str


class CursoCreate(CursoBase):
    pass


class CursoUpdate(BaseModel):
    model_config = {"populate_by_name": True}

    nombre_curso: Optional[str] = Field(None, alias="nombreCurso")
    nombre_docente: Optional[str] = Field(None, alias="nombreDocente")
    horario: Optional[str] = None
    color: Optional[int] = None


class Curso(CursoBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
