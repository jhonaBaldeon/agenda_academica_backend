from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.curso_schema import Curso, CursoCreate, CursoUpdate
from ..schemas.actividad_schema import Actividad, ActividadCreate, ActividadUpdate
from ..repositories.dependencies import get_curso_repository, get_actividad_repository
from ..repositories.curso_repository import CursoRepository
from ..repositories.actividad_repository import ActividadRepository

router = APIRouter(prefix="/cursos", tags=["cursos"])


@router.post("", response_model=Curso, status_code=201)
def create_curso(
    curso: CursoCreate, repo: CursoRepository = Depends(get_curso_repository)
):
    return repo.create(curso)


@router.get("", response_model=List[Curso])
def get_cursos(
    docente_id: str = None, repo: CursoRepository = Depends(get_curso_repository)
):
    if docente_id:
        return repo.get_by_docente(docente_id)
    return repo.get_all()


@router.get("/{curso_id}", response_model=Curso)
def get_curso(curso_id: str, repo: CursoRepository = Depends(get_curso_repository)):
    curso = repo.get_by_id(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.put("/{curso_id}", response_model=Curso)
def update_curso(
    curso_id: str,
    curso_update: CursoUpdate,
    repo: CursoRepository = Depends(get_curso_repository),
):
    curso = repo.update(curso_id, curso_update)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.delete("/{curso_id}", status_code=204)
def delete_curso(
    curso_id: str,
    curso_repo: CursoRepository = Depends(get_curso_repository),
    actividad_repo: ActividadRepository = Depends(get_actividad_repository),
):
    actividad_repo.delete_by_curso(curso_id)
    if not curso_repo.delete(curso_id):
        raise HTTPException(status_code=404, detail="Curso no encontrado")


@router.post("/{curso_id}/actividades", response_model=Actividad, status_code=201)
def create_actividad(
    curso_id: str,
    actividad: ActividadCreate,
    repo: ActividadRepository = Depends(get_actividad_repository),
):
    actividad.curso_id = curso_id
    return repo.create(actividad)


@router.get("/{curso_id}/actividades", response_model=List[Actividad])
def get_actividades_curso(
    curso_id: str, repo: ActividadRepository = Depends(get_actividad_repository)
):
    return repo.get_by_curso(curso_id)


@router.put("/{curso_id}/actividades/{actividad_id}", response_model=Actividad)
def update_actividad(
    curso_id: str,
    actividad_id: str,
    actividad_update: ActividadUpdate,
    repo: ActividadRepository = Depends(get_actividad_repository),
):
    actividad = repo.update(actividad_id, actividad_update)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    return actividad


@router.delete("/{curso_id}/actividades/{actividad_id}", status_code=204)
def delete_actividad(
    curso_id: str,
    actividad_id: str,
    repo: ActividadRepository = Depends(get_actividad_repository),
):
    if not repo.delete(actividad_id):
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
