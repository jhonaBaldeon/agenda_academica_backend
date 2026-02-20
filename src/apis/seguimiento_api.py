from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.seguimiento_schema import (
    Seguimiento,
    SeguimientoCreate,
    SeguimientoUpdate,
)
from ..repositories.dependencies import get_seguimiento_repository
from ..repositories.seguimiento_repository import SeguimientoRepository

router = APIRouter(prefix="/seguimientos", tags=["seguimientos"])


@router.post("", response_model=Seguimiento, status_code=201)
def create_seguimiento(
    seguimiento: SeguimientoCreate,
    repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    existing = repo.get_by_alumno_and_actividad(
        seguimiento.alumno_id, seguimiento.actividad_id
    )
    if existing:
        return existing
    return repo.create(seguimiento)


@router.get("", response_model=List[Seguimiento])
def get_seguimientos(
    alumno_id: str = None,
    curso_id: str = None,
    repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    if alumno_id and curso_id:
        return repo.get_by_alumno_and_curso(alumno_id, curso_id)
    if alumno_id:
        return repo.get_by_alumno(alumno_id)
    if curso_id:
        return repo.get_by_curso(curso_id)
    return repo.get_all()


@router.get("/{seguimiento_id}", response_model=Seguimiento)
def get_seguimiento(
    seguimiento_id: str,
    repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    seguimiento = repo.get_by_id(seguimiento_id)
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return seguimiento


@router.put("/{seguimiento_id}", response_model=Seguimiento)
def update_seguimiento(
    seguimiento_id: str,
    seguimiento_update: SeguimientoUpdate,
    repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    seguimiento = repo.update(seguimiento_id, seguimiento_update)
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return seguimiento


@router.delete("/{seguimiento_id}", status_code=204)
def delete_seguimiento(
    seguimiento_id: str,
    repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    if not repo.delete(seguimiento_id):
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
