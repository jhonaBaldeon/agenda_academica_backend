from pydantic import BaseModel
from typing import Optional


class EstadisticaCurso(BaseModel):
    curso_id: str
    curso_nombre: str
    color: int
    total_alumnos: int
    completados: int
    incompletos: int
    no_realizados: int

    @property
    def total_actividades(self) -> int:
        return self.completados + self.incompletos + self.no_realizados

    @property
    def porcentaje_completados(self) -> float:
        if self.total_actividades == 0:
            return 0.0
        return (self.completados / self.total_actividades) * 100

    @property
    def porcentaje_incompletos(self) -> float:
        if self.total_actividades == 0:
            return 0.0
        return (self.incompletos / self.total_actividades) * 100

    @property
    def porcentaje_no_realizados(self) -> float:
        if self.total_actividades == 0:
            return 0.0
        return (self.no_realizados / self.total_actividades) * 100

    @property
    def rendimiento(self) -> str:
        porcentaje = self.porcentaje_completados
        if porcentaje >= 90:
            return "Excelente"
        elif porcentaje >= 60:
            return "Regular"
        else:
            return "En proceso de Aprendizaje"


class EstadisticaGlobal(BaseModel):
    total_alumnos: int
    total_cursos: int
    total_completados: int
    total_incompletos: int
    total_no_realizados: int

    @property
    def total_actividades(self) -> int:
        return (
            self.total_completados + self.total_incompletos + self.total_no_realizados
        )

    @property
    def porcentaje_completados(self) -> float:
        if self.total_actividades == 0:
            return 0.0
        return (self.total_completados / self.total_actividades) * 100

    @property
    def rendimiento_global(self) -> str:
        porcentaje = self.porcentaje_completados
        if porcentaje >= 90:
            return "Excelente"
        elif porcentaje >= 60:
            return "Regular"
        else:
            return "En proceso de Aprendizaje"
