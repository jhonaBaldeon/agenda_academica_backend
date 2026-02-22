from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.alumno_schema import Alumno, AlumnoCreate, AlumnoUpdate
from ..repositories.dependencies import (
    get_alumno_repository,
    get_seguimiento_repository,
    get_actividad_repository,
)
from ..repositories.alumno_repository import AlumnoRepository
from ..repositories.seguimiento_repository import SeguimientoRepository
from ..repositories.actividad_repository import ActividadRepository

router = APIRouter(prefix="/alumnos", tags=["alumnos"])


@router.post("", response_model=Alumno, status_code=201)
def create_alumno(
    alumno: AlumnoCreate,
    repo: AlumnoRepository = Depends(get_alumno_repository),
    seguimiento_repo: SeguimientoRepository = Depends(get_seguimiento_repository),
    actividad_repo: ActividadRepository = Depends(get_actividad_repository),
):
    nuevo_alumno = repo.create(alumno)

    # Crear seguimientos para todas las actividades existentes
    try:
        actividades = actividad_repo.get_all()
        for actividad in actividades:
            # Verificar si ya existe un seguimiento para esta actividad y alumno
            existing = seguimiento_repo.get_by_alumno_and_actividad(
                nuevo_alumno.id, actividad.id
            )
            if not existing:
                from ..schemas.seguimiento_schema import (
                    SeguimientoCreate,
                    EstadoSeguimiento,
                )

                seguimiento = SeguimientoCreate(
                    alumno_id=nuevo_alumno.id,
                    alumno_nombre=nuevo_alumno.nombres,
                    actividad_id=actividad.id,
                    actividad_titulo=actividad.titulo,
                    actividad_descripcion=actividad.descripcion,
                    actividad_fecha_entrega=actividad.fecha_entrega,
                    curso_id=actividad.curso_id,
                    curso_nombre="",
                    estado=EstadoSeguimiento.incompleto,
                    observaciones=None,
                )
                seguimiento_repo.create(seguimiento)
    except Exception as e:
        print(f"Error creating seguimientos: {e}")

    return nuevo_alumno


@router.get("", response_model=List[Alumno])
def get_alumnos(repo: AlumnoRepository = Depends(get_alumno_repository)):
    return repo.get_all()


@router.get("/search", response_model=List[Alumno])
def search_alumnos(q: str, repo: AlumnoRepository = Depends(get_alumno_repository)):
    return repo.search(q)


@router.get("/{alumno_id}", response_model=Alumno)
def get_alumno(alumno_id: str, repo: AlumnoRepository = Depends(get_alumno_repository)):
    alumno = repo.get_by_id(alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.put("/{alumno_id}", response_model=Alumno)
def update_alumno(
    alumno_id: str,
    alumno_update: AlumnoUpdate,
    repo: AlumnoRepository = Depends(get_alumno_repository),
):
    alumno = repo.update(alumno_id, alumno_update)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.delete("/{alumno_id}", status_code=204)
def delete_alumno(
    alumno_id: str, repo: AlumnoRepository = Depends(get_alumno_repository)
):
    if not repo.delete(alumno_id):
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
