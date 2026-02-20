from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.alumno_schema import Alumno, AlumnoCreate, AlumnoUpdate
from ..repositories.dependencies import get_alumno_repository
from ..repositories.alumno_repository import AlumnoRepository

router = APIRouter(prefix="/alumnos", tags=["alumnos"])


@router.post("", response_model=Alumno, status_code=201)
def create_alumno(
    alumno: AlumnoCreate, repo: AlumnoRepository = Depends(get_alumno_repository)
):
    return repo.create(alumno)


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
