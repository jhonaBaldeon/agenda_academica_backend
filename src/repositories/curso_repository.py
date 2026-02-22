from datetime import datetime
from typing import List, Optional
from google.cloud import firestore
from ..schemas.curso_schema import Curso, CursoCreate, CursoUpdate
from ..firebase_config import get_db


class CursoRepository:
    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = get_db()
        return self._db

    def create(self, curso: CursoCreate) -> Curso:
        now = datetime.now()
        doc_ref = self.db.collection("cursos").document()
        nuevo_curso = Curso(
            id=doc_ref.id,
            nombre_curso=curso.nombre_curso,
            nombre_docente=curso.nombre_docente,
            horario=curso.horario,
            color=curso.color,
            docente_id=curso.docente_id,
            created_at=now,
        )
        doc_ref.set(
            {
                "nombre_curso": nuevo_curso.nombre_curso,
                "nombre_docente": nuevo_curso.nombre_docente,
                "horario": nuevo_curso.horario,
                "color": nuevo_curso.color,
                "docente_id": nuevo_curso.docente_id,
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )
        return nuevo_curso

    def get_all(self) -> List[Curso]:
        docs = (
            self.db.collection("cursos")
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .stream()
        )
        cursos = []
        for doc in docs:
            data = doc.to_dict()
            created_at = data.get("created_at")
            if created_at and hasattr(created_at, "timestamp"):
                created_at = created_at.timestamp()
            elif isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            else:
                created_at = datetime.now()

            cursos.append(
                Curso(
                    id=doc.id,
                    nombre_curso=data.get("nombre_curso", ""),
                    nombre_docente=data.get("nombre_docente", ""),
                    horario=data.get("horario", ""),
                    color=data.get("color", 0),
                    docente_id=data.get("docente_id", ""),
                    created_at=created_at,
                )
            )
        return cursos

    def get_by_id(self, curso_id: str) -> Optional[Curso]:
        doc = self.db.collection("cursos").document(curso_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        created_at = data.get("created_at")
        if created_at and hasattr(created_at, "timestamp"):
            created_at = created_at.timestamp()
        elif isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        else:
            created_at = datetime.now()

        return Curso(
            id=doc.id,
            nombre_curso=data.get("nombre_curso", ""),
            nombre_docente=data.get("nombre_docente", ""),
            horario=data.get("horario", ""),
            color=data.get("color", 0),
            docente_id=data.get("docente_id", ""),
            created_at=created_at,
        )

    def get_by_docente(self, docente_id: str) -> List[Curso]:
        docs = (
            self.db.collection("cursos").where("docente_id", "==", docente_id).stream()
        )
        cursos = []
        for doc in docs:
            data = doc.to_dict()
            created_at = data.get("created_at")
            if created_at and hasattr(created_at, "timestamp"):
                created_at = created_at.timestamp()
            elif isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            else:
                created_at = datetime.now()

            cursos.append(
                Curso(
                    id=doc.id,
                    nombre_curso=data.get("nombre_curso", ""),
                    nombre_docente=data.get("nombre_docente", ""),
                    horario=data.get("horario", ""),
                    color=data.get("color", 0),
                    docente_id=data.get("docente_id", ""),
                    created_at=created_at,
                )
            )
        return cursos

    def update(self, curso_id: str, curso_update: CursoUpdate) -> Optional[Curso]:
        doc_ref = self.db.collection("cursos").document(curso_id)
        if not doc_ref.get().exists:
            return None

        update_data = curso_update.model_dump(exclude_unset=True)

        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.update(update_data)

        return self.get_by_id(curso_id)

    def delete(self, curso_id: str) -> bool:
        doc_ref = self.db.collection("cursos").document(curso_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
