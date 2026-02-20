from fastapi import APIRouter, Depends, HTTPException
from ..schemas.estadistica_schema import EstadisticaCurso, EstadisticaGlobal
from ..services.estadistica_service import get_estadistica_service, EstadisticaService

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


@router.get("/global", response_model=EstadisticaGlobal)
def get_estadisticas_globales(
    service: EstadisticaService = Depends(get_estadistica_service),
):
    return service.get_estadisticas_globales()


@router.get("/curso/{curso_id}", response_model=EstadisticaCurso)
def get_estadisticas_curso(
    curso_id: str, service: EstadisticaService = Depends(get_estadistica_service)
):
    estadistica = service.get_estadisticas_por_curso(curso_id)
    if not estadistica:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return estadistica
