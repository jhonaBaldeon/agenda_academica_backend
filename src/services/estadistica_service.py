from typing import List
from ..repositories.dependencies import (
    get_curso_repository,
    get_alumno_repository,
    get_seguimiento_repository,
    get_actividad_repository,
)
from ..schemas.estadistica_schema import EstadisticaCurso, EstadisticaGlobal
from ..schemas.seguimiento_schema import EstadoSeguimiento


class EstadisticaService:
    def get_estadisticas_por_curso(self, curso_id: str) -> EstadisticaCurso:
        curso_repo = get_curso_repository()
        seguimiento_repo = get_seguimiento_repository()

        curso = curso_repo.get_by_id(curso_id)
        if not curso:
            return None

        seguimientos = seguimiento_repo.get_by_curso(curso_id)

        total_alumnos = (
            len(set(s.alumno_id for s in seguimientos)) if seguimientos else 0
        )
        completados = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.completado
        )
        incompletos = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.incompleto
        )
        no_realizados = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.no_realizado
        )

        return EstadisticaCurso(
            curso_id=curso_id,
            curso_nombre=curso.nombre_curso,
            color=curso.color,
            total_alumnos=total_alumnos,
            completados=completados,
            incompletos=incompletos,
            no_realizados=no_realizados,
        )

    def get_estadisticas_globales(self) -> EstadisticaGlobal:
        curso_repo = get_curso_repository()
        alumno_repo = get_alumno_repository()
        seguimiento_repo = get_seguimiento_repository()

        cursos = curso_repo.get_all()
        alumnos = alumno_repo.get_all()
        seguimientos = seguimiento_repo.get_all()

        total_completados = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.completado
        )
        total_incompletos = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.incompleto
        )
        total_no_realizados = sum(
            1 for s in seguimientos if s.estado == EstadoSeguimiento.no_realizado
        )

        return EstadisticaGlobal(
            total_alumnos=len(alumnos),
            total_cursos=len(cursos),
            total_completados=total_completados,
            total_incompletos=total_incompletos,
            total_no_realizados=total_no_realizados,
        )


estadistica_service = EstadisticaService()


def get_estadistica_service() -> EstadisticaService:
    return estadistica_service
