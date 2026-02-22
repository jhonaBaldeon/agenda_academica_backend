from datetime import datetime
from typing import List, Optional
from google.cloud import firestore
from ..schemas.alumno_schema import Alumno, AlumnoCreate, AlumnoUpdate
from ..firebase_config import get_db


class AlumnoRepository:
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

    def create(self, alumno: AlumnoCreate) -> Alumno:
        doc_ref = self.db.collection("alumnos").document()
        now = datetime.now()

        nuevo_alumno = Alumno(
            id=doc_ref.id,
            nombres=alumno.nombres,
            apellido_paterno=alumno.apellido_paterno,
            apellido_materno=alumno.apellido_materno,
            grado=alumno.grado,
            seccion=alumno.seccion,
            padre_id=alumno.padre_id,
            created_at=now,
        )

        doc_ref.set(
            {
                "nombres": nuevo_alumno.nombres,
                "apellido_paterno": nuevo_alumno.apellido_paterno,
                "apellido_materno": nuevo_alumno.apellido_materno,
                "grado": nuevo_alumno.grado,
                "seccion": nuevo_alumno.seccion,
                "padre_id": nuevo_alumno.padre_id,
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )

        return nuevo_alumno

    def get_all(self) -> List[Alumno]:
        docs = (
            self.db.collection("alumnos")
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .stream()
        )
        alumnos = []
        for doc in docs:
            data = doc.to_dict()
            created_at = self._parse_fecha(data.get("created_at"))

            # Calcular nombre completo
            nombres = data.get("nombres", "")
            apellido_paterno = data.get("apellido_paterno", "")
            apellido_materno = data.get("apellido_materno", "")
            nombre_completo = f"{nombres} {apellido_paterno} {apellido_materno}".strip()

            alumnos.append(
                Alumno(
                    id=doc.id,
                    nombres=nombres,
                    apellido_paterno=apellido_paterno,
                    apellido_materno=apellido_materno,
                    grado=data.get("grado", ""),
                    seccion=data.get("seccion", ""),
                    padre_id=data.get("padre_id", ""),
                    created_at=created_at,
                )
            )
        return sorted(alumnos, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, alumno_id: str) -> Optional[Alumno]:
        doc = self.db.collection("alumnos").document(alumno_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        created_at = self._parse_fecha(data.get("created_at"))

        return Alumno(
            id=doc.id,
            nombres=data.get("nombres", ""),
            apellido_paterno=data.get("apellido_paterno", ""),
            apellido_materno=data.get("apellido_materno", ""),
            grado=data.get("grado", ""),
            seccion=data.get("seccion", ""),
            padre_id=data.get("padre_id", ""),
            created_at=created_at,
        )

    def update(self, alumno_id: str, alumno_update: AlumnoUpdate) -> Optional[Alumno]:
        doc_ref = self.db.collection("alumnos").document(alumno_id)
        if not doc_ref.get().exists:
            return None

        update_data = alumno_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.update(update_data)

        return self.get_by_id(alumno_id)

    def delete(self, alumno_id: str) -> bool:
        doc_ref = self.db.collection("alumnos").document(alumno_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True

    def search(self, query: str) -> List[Alumno]:
        query_lower = query.lower()
        docs = self.db.collection("alumnos").stream()

        resultados = []
        for doc in docs:
            data = doc.to_dict()
            nombres = data.get("nombres", "").lower()
            apellido_paterno = data.get("apellido_paterno", "").lower()
            apellido_materno = data.get("apellido_materno", "").lower()

            if (
                query_lower in nombres
                or query_lower in apellido_paterno
                or query_lower in apellido_materno
            ):
                created_at = self._parse_fecha(data.get("created_at"))
                resultados.append(
                    Alumno(
                        id=doc.id,
                        nombres=data.get("nombres", ""),
                        apellido_paterno=data.get("apellido_paterno", ""),
                        apellido_materno=data.get("apellido_materno", ""),
                        grado=data.get("grado", ""),
                        seccion=data.get("seccion", ""),
                        padre_id=data.get("padre_id", ""),
                        created_at=created_at,
                    )
                )

        return resultados
