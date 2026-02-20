from datetime import datetime
from typing import List, Optional
import uuid
from ..schemas.seguimiento_schema import (
    Seguimiento,
    SeguimientoCreate,
    SeguimientoUpdate,
    EstadoSeguimiento,
)


class SeguimientoRepository:
    def __init__(self):
        self._seguimientos: List[Seguimiento] = []

    def create(self, seguimiento: SeguimientoCreate) -> Seguimiento:
        now = datetime.now()
        nuevo_seguimiento = Seguimiento(
            id=str(uuid.uuid4()),
            alumno_id=seguimiento.alumno_id,
            alumno_nombre=seguimiento.alumno_nombre,
            actividad_id=seguimiento.actividad_id,
            actividad_titulo=seguimiento.actividad_titulo,
            actividad_descripcion=seguimiento.actividad_descripcion,
            actividad_fecha_entrega=seguimiento.actividad_fecha_entrega,
            curso_id=seguimiento.curso_id,
            curso_nombre=seguimiento.curso_nombre,
            estado=seguimiento.estado,
            observaciones=seguimiento.observaciones,
            fecha_completado=None,
            created_at=now,
            updated_at=now,
        )
        self._seguimientos.append(nuevo_seguimiento)
        return nuevo_seguimiento

    def get_all(self) -> List[Seguimiento]:
        return sorted(self._seguimientos, key=lambda x: x.updated_at, reverse=True)

    def get_by_id(self, seguimiento_id: str) -> Optional[Seguimiento]:
        for seguimiento in self._seguimientos:
            if seguimiento.id == seguimiento_id:
                return seguimiento
        return None

    def get_by_alumno(self, alumno_id: str) -> List[Seguimiento]:
        return [s for s in self._seguimientos if s.alumno_id == alumno_id]

    def get_by_curso(self, curso_id: str) -> List[Seguimiento]:
        return [s for s in self._seguimientos if s.curso_id == curso_id]

    def get_by_alumno_and_curso(
        self, alumno_id: str, curso_id: str
    ) -> List[Seguimiento]:
        return [
            s
            for s in self._seguimientos
            if s.alumno_id == alumno_id and s.curso_id == curso_id
        ]

    def get_by_alumno_and_actividad(
        self, alumno_id: str, actividad_id: str
    ) -> Optional[Seguimiento]:
        for s in self._seguimientos:
            if s.alumno_id == alumno_id and s.actividad_id == actividad_id:
                return s
        return None

    def update(
        self, seguimiento_id: str, seguimiento_update: SeguimientoUpdate
    ) -> Optional[Seguimiento]:
        for i, seguimiento in enumerate(self._seguimientos):
            if seguimiento.id == seguimiento_id:
                update_data = seguimiento_update.model_dump(exclude_unset=True)
                if "estado" in update_data:
                    if update_data["estado"] == EstadoSeguimiento.completado:
                        self._seguimientos[i].fecha_completado = datetime.now()
                    else:
                        self._seguimientos[i].fecha_completado = None
                for key, value in update_data.items():
                    setattr(self._seguimientos[i], key, value)
                self._seguimientos[i].updated_at = datetime.now()
                return self._seguimientos[i]
        return None

    def delete(self, seguimiento_id: str) -> bool:
        for i, seguimiento in enumerate(self._seguimientos):
            if seguimiento.id == seguimiento_id:
                del self._seguimientos[i]
                return True
        return False
