from datetime import datetime
from typing import List, Optional
import uuid
from ..schemas.curso_schema import Curso, CursoCreate, CursoUpdate


class CursoRepository:
    def __init__(self):
        self._cursos: List[Curso] = []

    def create(self, curso: CursoCreate) -> Curso:
        now = datetime.now()
        nuevo_curso = Curso(
            id=str(uuid.uuid4()),
            nombre_curso=curso.nombre_curso,
            nombre_docente=curso.nombre_docente,
            horario=curso.horario,
            color=curso.color,
            docente_id=curso.docente_id,
            created_at=now,
        )
        self._cursos.append(nuevo_curso)
        return nuevo_curso

    def get_all(self) -> List[Curso]:
        return sorted(self._cursos, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, curso_id: str) -> Optional[Curso]:
        for curso in self._cursos:
            if curso.id == curso_id:
                return curso
        return None

    def get_by_docente(self, docente_id: str) -> List[Curso]:
        return [c for c in self._cursos if c.docente_id == docente_id]

    def update(self, curso_id: str, curso_update: CursoUpdate) -> Optional[Curso]:
        for i, curso in enumerate(self._cursos):
            if curso.id == curso_id:
                update_data = curso_update.model_dump(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(self._cursos[i], key, value)
                return self._cursos[i]
        return None

    def delete(self, curso_id: str) -> bool:
        for i, curso in enumerate(self._cursos):
            if curso.id == curso_id:
                del self._cursos[i]
                return True
        return False
