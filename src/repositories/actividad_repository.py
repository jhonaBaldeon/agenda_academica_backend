from datetime import datetime
from typing import List, Optional
import uuid
from ..schemas.actividad_schema import (
    Actividad,
    ActividadCreate,
    ActividadUpdate,
    EstadoActividad,
)


class ActividadRepository:
    def __init__(self):
        self._actividades: List[Actividad] = []

    def create(self, actividad: ActividadCreate) -> Actividad:
        now = datetime.now()
        nueva_actividad = Actividad(
            id=str(uuid.uuid4()),
            curso_id=actividad.curso_id,
            titulo=actividad.titulo,
            descripcion=actividad.descripcion,
            fecha_entrega=actividad.fecha_entrega,
            prioridad=actividad.prioridad,
            estado=EstadoActividad.incompleto,
            created_at=now,
        )
        self._actividades.append(nueva_actividad)
        return nueva_actividad

    def get_all(self) -> List[Actividad]:
        return sorted(self._actividades, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, actividad_id: str) -> Optional[Actividad]:
        for actividad in self._actividades:
            if actividad.id == actividad_id:
                return actividad
        return None

    def get_by_curso(self, curso_id: str) -> List[Actividad]:
        return [a for a in self._actividades if a.curso_id == curso_id]

    def update(
        self, actividad_id: str, actividad_update: ActividadUpdate
    ) -> Optional[Actividad]:
        for i, actividad in enumerate(self._actividades):
            if actividad.id == actividad_id:
                update_data = actividad_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(self._actividades[i], key, value)
                return self._actividades[i]
        return None

    def delete(self, actividad_id: str) -> bool:
        for i, actividad in enumerate(self._actividades):
            if actividad.id == actividad_id:
                del self._actividades[i]
                return True
        return False

    def delete_by_curso(self, curso_id: str) -> int:
        original_len = len(self._actividades)
        self._actividades = [a for a in self._actividades if a.curso_id != curso_id]
        return original_len - len(self._actividades)
