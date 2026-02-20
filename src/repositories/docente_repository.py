from datetime import datetime
from typing import List, Optional
import uuid
from ..schemas.docente_schema import Docente, DocenteCreate, DocenteUpdate


class DocenteRepository:
    def __init__(self):
        self._docentes: List[Docente] = []

    def create(self, docente: DocenteCreate) -> Docente:
        now = datetime.now()
        nuevo_docente = Docente(
            id=str(uuid.uuid4()),
            email=docente.email,
            nombre=docente.nombre,
            activo=docente.activo,
            fecha_registro=now,
        )
        self._docentes.append(nuevo_docente)
        return nuevo_docente

    def get_all(self) -> List[Docente]:
        return sorted(self._docentes, key=lambda x: x.fecha_registro, reverse=True)

    def get_by_id(self, docente_id: str) -> Optional[Docente]:
        for docente in self._docentes:
            if docente.id == docente_id:
                return docente
        return None

    def get_by_email(self, email: str) -> Optional[Docente]:
        for docente in self._docentes:
            if docente.email == email:
                return docente
        return None

    def update(
        self, docente_id: str, docente_update: DocenteUpdate
    ) -> Optional[Docente]:
        for i, docente in enumerate(self._docentes):
            if docente.id == docente_id:
                update_data = docente_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(self._docentes[i], key, value)
                return self._docentes[i]
        return None

    def delete(self, docente_id: str) -> bool:
        for i, docente in enumerate(self._docentes):
            if docente.id == docente_id:
                del self._docentes[i]
                return True
        return False
