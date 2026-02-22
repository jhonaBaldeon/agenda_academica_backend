from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Any
from ..schemas.curso_schema import Curso, CursoCreate, CursoUpdate
from ..schemas.actividad_schema import Actividad, ActividadCreate, ActividadUpdate
from ..repositories.dependencies import (
    get_curso_repository,
    get_actividad_repository,
    get_seguimiento_repository,
    get_alumno_repository,
)
from ..repositories.curso_repository import CursoRepository
from ..repositories.actividad_repository import ActividadRepository
from ..repositories.seguimiento_repository import SeguimientoRepository
from ..repositories.alumno_repository import AlumnoRepository

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
    body: dict = Body(...),
    repo: CursoRepository = Depends(get_curso_repository),
):
    # Convertir camelCase a snake_case
    data = {}
    for key, value in body.items():
        if key == "nombreCurso":
            data["nombre_curso"] = value
        elif key == "nombreDocente":
            data["nombre_docente"] = value
        else:
            data[key] = value

    curso_update = CursoUpdate(**data)
    curso = repo.update(curso_id, curso_update)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.delete("/{curso_id}", status_code=204)
def delete_curso(
    curso_id: str,
    curso_repo: CursoRepository = Depends(get_curso_repository),
    actividad_repo: ActividadRepository = Depends(get_actividad_repository),
    seguimiento_repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    # Primero eliminar todos los seguimientos del curso
    seguimiento_repo.delete_by_curso(curso_id)
    # Eliminar las actividades del curso
    actividad_repo.delete_by_curso(curso_id)
    if not curso_repo.delete(curso_id):
        raise HTTPException(status_code=404, detail="Curso no encontrado")


@router.post("/{curso_id}/actividades", response_model=Actividad, status_code=201)
def create_actividad(
    curso_id: str,
    actividad: ActividadCreate,
    actividad_repo: ActividadRepository = Depends(get_actividad_repository),
    seguimiento_repo: SeguimientoRepository = Depends(get_seguimiento_repository),
    alumno_repo: AlumnoRepository = Depends(get_alumno_repository),
    curso_repo: CursoRepository = Depends(get_curso_repository),
):
    actividad.curso_id = curso_id
    nueva_actividad = actividad_repo.create(actividad)

    # Obtener el curso para obtener el nombre
    curso = curso_repo.get_by_id(curso_id)
    curso_nombre = curso.nombre_curso if curso else "Curso"

    # Obtener todos los alumnos y crear seguimientos
    try:
        alumnos = alumno_repo.get_all()
        for alumno in alumnos:
            # Verificar si ya existe un seguimiento para esta actividad y alumno
            existing = seguimiento_repo.get_by_alumno_and_actividad(
                alumno.id, nueva_actividad.id
            )
            if not existing:
                from ..schemas.seguimiento_schema import (
                    SeguimientoCreate,
                    EstadoSeguimiento,
                )

                seguimiento = SeguimientoCreate(
                    alumno_id=alumno.id,
                    alumno_nombre=alumno.nombres,
                    actividad_id=nueva_actividad.id,
                    actividad_titulo=nueva_actividad.titulo,
                    actividad_descripcion=nueva_actividad.descripcion,
                    actividad_fecha_entrega=nueva_actividad.fecha_entrega,
                    curso_id=curso_id,
                    curso_nombre=curso_nombre,
                    estado=EstadoSeguimiento.incompleto,
                    observaciones=None,
                )
                seguimiento_repo.create(seguimiento)
    except Exception as e:
        print(f"Error creating seguimientos: {e}")

    return nueva_actividad


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
    seguimiento_repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    actividad = repo.update(actividad_id, actividad_update)
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    # Actualizar seguimientos relacionados
    try:
        update_data = actividad_update.model_dump(exclude_unset=True)

        # Actualizar titulo en seguimientos
        if "titulo" in update_data:
            seguimientos = seguimiento_repo.get_by_actividad(actividad_id)
            for seg in seguimientos:
                from ..schemas.seguimiento_schema import SeguimientoUpdate

                seg_update = SeguimientoUpdate(
                    actividad_titulo=update_data["titulo"],
                )
                seguimiento_repo.update(seg.id, seg_update)

        # Actualizar descripcion en seguimientos
        if "descripcion" in update_data:
            seguimientos = seguimiento_repo.get_by_actividad(actividad_id)
            for seg in seguimientos:
                from ..schemas.seguimiento_schema import SeguimientoUpdate

                seg_update = SeguimientoUpdate(
                    actividad_descripcion=update_data["descripcion"],
                )
                seguimiento_repo.update(seg.id, seg_update)

        # Actualizar fecha_entrega en seguimientos
        if "fecha_entrega" in update_data:
            fecha = update_data["fecha_entrega"]
            if isinstance(fecha, str):
                from datetime import datetime

                fecha = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            seguimientos = seguimiento_repo.get_by_actividad(actividad_id)
            for seg in seguimientos:
                from ..schemas.seguimiento_schema import SeguimientoUpdate

                seg_update = SeguimientoUpdate(
                    actividad_fecha_entrega=fecha,
                )
                seguimiento_repo.update(seg.id, seg_update)

    except Exception as e:
        print(f"Error updating seguimientos: {e}")

    return actividad


@router.delete("/{curso_id}/actividades/{actividad_id}", status_code=204)
def delete_actividad(
    curso_id: str,
    actividad_id: str,
    repo: ActividadRepository = Depends(get_actividad_repository),
    seguimiento_repo: SeguimientoRepository = Depends(get_seguimiento_repository),
):
    # Primero eliminar todos los seguimientos de la actividad
    seguimiento_repo.delete_by_actividad(actividad_id)
    if not repo.delete(actividad_id):
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
