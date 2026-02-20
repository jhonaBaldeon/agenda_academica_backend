from .curso_repository import CursoRepository
from .actividad_repository import ActividadRepository
from .alumno_repository import AlumnoRepository
from .seguimiento_repository import SeguimientoRepository
from .docente_repository import DocenteRepository


curso_repository = CursoRepository()
actividad_repository = ActividadRepository()
alumno_repository = AlumnoRepository()
seguimiento_repository = SeguimientoRepository()
docente_repository = DocenteRepository()


def get_curso_repository() -> CursoRepository:
    return curso_repository


def get_actividad_repository() -> ActividadRepository:
    return actividad_repository


def get_alumno_repository() -> AlumnoRepository:
    return alumno_repository


def get_seguimiento_repository() -> SeguimientoRepository:
    return seguimiento_repository


def get_docente_repository() -> DocenteRepository:
    return docente_repository
