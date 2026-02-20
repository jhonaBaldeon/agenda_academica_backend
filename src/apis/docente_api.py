from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.docente_schema import Docente, DocenteCreate, DocenteUpdate
from ..repositories.dependencies import get_docente_repository
from ..repositories.docente_repository import DocenteRepository

router = APIRouter(prefix="/docentes", tags=["docentes"])


@router.post("", response_model=Docente, status_code=201)
def create_docente(
    docente: DocenteCreate, repo: DocenteRepository = Depends(get_docente_repository)
):
    existing = repo.get_by_email(docente.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return repo.create(docente)


@router.get("", response_model=List[Docente])
def get_docentes(repo: DocenteRepository = Depends(get_docente_repository)):
    return repo.get_all()


@router.get("/{docente_id}", response_model=Docente)
def get_docente(
    docente_id: str, repo: DocenteRepository = Depends(get_docente_repository)
):
    docente = repo.get_by_id(docente_id)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente


@router.put("/{docente_id}", response_model=Docente)
def update_docente(
    docente_id: str,
    docente_update: DocenteUpdate,
    repo: DocenteRepository = Depends(get_docente_repository),
):
    docente = repo.update(docente_id, docente_update)
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    return docente


@router.delete("/{docente_id}", status_code=204)
def delete_docente(
    docente_id: str, repo: DocenteRepository = Depends(get_docente_repository)
):
    if not repo.delete(docente_id):
        raise HTTPException(status_code=404, detail="Docente no encontrado")
