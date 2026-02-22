from datetime import datetime
from typing import List, Optional
from google.cloud import firestore
from ..schemas.docente_schema import Docente, DocenteCreate, DocenteUpdate
from ..firebase_config import get_db


class DocenteRepository:
    def __init__(self):
        self._db = None

    @property
    def db(self):
        if self._db is None:
            self._db = get_db()
        return self._db

    def _parse_fecha(self, fecha):
        if fecha is None:
            return datetime.now()
        if hasattr(fecha, "timestamp"):
            return fecha.timestamp()
        elif isinstance(fecha, str):
            try:
                return datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            except:
                return datetime.now()
        return datetime.now()

    def create(self, docente: DocenteCreate) -> Docente:
        doc_ref = self.db.collection("docentes").document()
        now = datetime.now()

        nuevo_docente = Docente(
            id=doc_ref.id,
            email=docente.email,
            nombre=docente.nombre,
            activo=docente.activo,
            fecha_registro=now,
        )

        doc_ref.set(
            {
                "email": nuevo_docente.email,
                "nombre": nuevo_docente.nombre,
                "activo": nuevo_docente.activo,
                "fecha_registro": firestore.SERVER_TIMESTAMP,
            }
        )

        return nuevo_docente

    def get_all(self) -> List[Docente]:
        docs = (
            self.db.collection("docentes")
            .order_by("fecha_registro", direction=firestore.Query.DESCENDING)
            .stream()
        )
        docentes = []
        for doc in docs:
            data = doc.to_dict()
            fecha_registro = self._parse_fecha(data.get("fecha_registro"))
            docentes.append(
                Docente(
                    id=doc.id,
                    email=data.get("email", ""),
                    nombre=data.get("nombre", ""),
                    activo=data.get("activo", True),
                    fecha_registro=fecha_registro,
                )
            )
        return sorted(docentes, key=lambda x: x.fecha_registro, reverse=True)

    def get_by_id(self, docente_id: str) -> Optional[Docente]:
        doc = self.db.collection("docentes").document(docente_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        fecha_registro = self._parse_fecha(data.get("fecha_registro"))

        return Docente(
            id=doc.id,
            email=data.get("email", ""),
            nombre=data.get("nombre", ""),
            activo=data.get("activo", True),
            fecha_registro=fecha_registro,
        )

    def get_by_email(self, email: str) -> Optional[Docente]:
        docs = self.db.collection("docentes").where("email", "==", email).stream()
        for doc in docs:
            data = doc.to_dict()
            fecha_registro = self._parse_fecha(data.get("fecha_registro"))
            return Docente(
                id=doc.id,
                email=data.get("email", ""),
                nombre=data.get("nombre", ""),
                activo=data.get("activo", True),
                fecha_registro=fecha_registro,
            )
        return None

    def update(
        self, docente_id: str, docente_update: DocenteUpdate
    ) -> Optional[Docente]:
        doc_ref = self.db.collection("docentes").document(docente_id)
        if not doc_ref.get().exists:
            return None

        update_data = docente_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.update(update_data)

        return self.get_by_id(docente_id)

    def delete(self, docente_id: str) -> bool:
        doc_ref = self.db.collection("docentes").document(docente_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
