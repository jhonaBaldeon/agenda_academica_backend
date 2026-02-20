from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocenteBase(BaseModel):
    email: str
    nombre: str
    activo: bool = True


class DocenteCreate(DocenteBase):
    pass


class DocenteUpdate(BaseModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    activo: Optional[bool] = None


class Docente(DocenteBase):
    id: str
    fecha_registro: datetime

    class Config:
        from_attributes = True
