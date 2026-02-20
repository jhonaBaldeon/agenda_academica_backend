from datetime import datetime
from typing import List, Optional
import uuid
from ..schemas.alumno_schema import Alumno, AlumnoCreate, AlumnoUpdate


class AlumnoRepository:
    def __init__(self):
        self._alumnos: List[Alumno] = []

    def create(self, alumno: AlumnoCreate) -> Alumno:
        now = datetime.now()
        nuevo_alumno = Alumno(
            id=str(uuid.uuid4()),
            nombres=alumno.nombres,
            apellido_paterno=alumno.apellido_paterno,
            apellido_materno=alumno.apellido_materno,
            grado=alumno.grado,
            seccion=alumno.seccion,
            padre_id=alumno.padre_id,
            created_at=now,
        )
        self._alumnos.append(nuevo_alumno)
        return nuevo_alumno

    def get_all(self) -> List[Alumno]:
        return sorted(self._alumnos, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, alumno_id: str) -> Optional[Alumno]:
        for alumno in self._alumnos:
            if alumno.id == alumno_id:
                return alumno
        return None

    def update(self, alumno_id: str, alumno_update: AlumnoUpdate) -> Optional[Alumno]:
        for i, alumno in enumerate(self._alumnos):
            if alumno.id == alumno_id:
                update_data = alumno_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(self._alumnos[i], key, value)
                return self._alumnos[i]
        return None

    def delete(self, alumno_id: str) -> bool:
        for i, alumno in enumerate(self._alumnos):
            if alumno.id == alumno_id:
                del self._alumnos[i]
                return True
        return False

    def search(self, query: str) -> List[Alumno]:
        query_lower = query.lower()
        return [
            a
            for a in self._alumnos
            if query_lower in a.nombres.lower()
            or query_lower in a.apellido_paterno.lower()
            or query_lower in a.apellido_materno.lower()
        ]
