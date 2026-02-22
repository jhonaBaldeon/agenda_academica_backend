from datetime import datetime
from typing import List, Optional
from google.cloud import firestore
from ..schemas.seguimiento_schema import (
    Seguimiento,
    SeguimientoCreate,
    SeguimientoUpdate,
    EstadoSeguimiento,
)
from ..firebase_config import get_db


class SeguimientoRepository:
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

    def _estado_from_string(self, value: str) -> EstadoSeguimiento:
        if value == "completado":
            return EstadoSeguimiento.completado
        elif value == "no_realizado":
            return EstadoSeguimiento.no_realizado
        return EstadoSeguimiento.incompleto

    def _estado_to_string(self, estado: EstadoSeguimiento) -> str:
        if estado == EstadoSeguimiento.completado:
            return "completado"
        elif estado == EstadoSeguimiento.no_realizado:
            return "no_realizado"
        return "incompleto"

    def _to_seguimiento(self, doc) -> Seguimiento:
        data = doc.to_dict()
        return Seguimiento(
            id=doc.id,
            alumno_id=data.get("alumno_id", ""),
            alumno_nombre=data.get("alumno_nombre", ""),
            actividad_id=data.get("actividad_id", ""),
            actividad_titulo=data.get("actividad_titulo", ""),
            actividad_descripcion=data.get("actividad_descripcion", ""),
            actividad_fecha_entrega=self._parse_fecha(
                data.get("actividad_fecha_entrega")
            ),
            curso_id=data.get("curso_id", ""),
            curso_nombre=data.get("curso_nombre", ""),
            estado=self._estado_from_string(data.get("estado", "incompleto")),
            observaciones=data.get("observaciones"),
            fecha_completado=self._parse_fecha(data.get("fecha_completado")),
            created_at=self._parse_fecha(data.get("created_at")),
            updated_at=self._parse_fecha(data.get("updated_at")),
        )

    def create(self, seguimiento: SeguimientoCreate) -> Seguimiento:
        doc_ref = self.db.collection("seguimientos").document()
        now = datetime.now()

        nuevo_seguimiento = Seguimiento(
            id=doc_ref.id,
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

        doc_ref.set(
            {
                "alumno_id": nuevo_seguimiento.alumno_id,
                "alumno_nombre": nuevo_seguimiento.alumno_nombre,
                "actividad_id": nuevo_seguimiento.actividad_id,
                "actividad_titulo": nuevo_seguimiento.actividad_titulo,
                "actividad_descripcion": nuevo_seguimiento.actividad_descripcion,
                "actividad_fecha_entrega": firestore.SERVER_TIMESTAMP,
                "curso_id": nuevo_seguimiento.curso_id,
                "curso_nombre": nuevo_seguimiento.curso_nombre,
                "estado": self._estado_to_string(nuevo_seguimiento.estado),
                "observaciones": nuevo_seguimiento.observaciones,
                "fecha_completado": None,
                "created_at": firestore.SERVER_TIMESTAMP,
                "updated_at": firestore.SERVER_TIMESTAMP,
            }
        )

        return nuevo_seguimiento

    def get_all(self) -> List[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .order_by("updated_at", direction=firestore.Query.DESCENDING)
            .stream()
        )
        seguimientos = [self._to_seguimiento(doc) for doc in docs]
        return sorted(seguimientos, key=lambda x: x.updated_at, reverse=True)

    def get_by_id(self, seguimiento_id: str) -> Optional[Seguimiento]:
        doc = self.db.collection("seguimientos").document(seguimiento_id).get()
        if not doc.exists:
            return None
        return self._to_seguimiento(doc)

    def get_by_alumno(self, alumno_id: str) -> List[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .where("alumno_id", "==", alumno_id)
            .stream()
        )
        return [self._to_seguimiento(doc) for doc in docs]

    def get_by_curso(self, curso_id: str) -> List[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .where("curso_id", "==", curso_id)
            .stream()
        )
        return [self._to_seguimiento(doc) for doc in docs]

    def get_by_alumno_and_curso(
        self, alumno_id: str, curso_id: str
    ) -> List[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .where("alumno_id", "==", alumno_id)
            .where("curso_id", "==", curso_id)
            .stream()
        )
        return [self._to_seguimiento(doc) for doc in docs]

    def get_by_alumno_and_actividad(
        self, alumno_id: str, actividad_id: str
    ) -> Optional[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .where("alumno_id", "==", alumno_id)
            .where("actividad_id", "==", actividad_id)
            .stream()
        )
        for doc in docs:
            return self._to_seguimiento(doc)
        return None

    def get_by_actividad(self, actividad_id: str) -> List[Seguimiento]:
        docs = (
            self.db.collection("seguimientos")
            .where("actividad_id", "==", actividad_id)
            .stream()
        )
        return [self._to_seguimiento(doc) for doc in docs]

    def update(
        self, seguimiento_id: str, seguimiento_update: SeguimientoUpdate
    ) -> Optional[Seguimiento]:
        doc_ref = self.db.collection("seguimientos").document(seguimiento_id)
        if not doc_ref.get().exists:
            return None

        update_data = seguimiento_update.model_dump(exclude_unset=True)

        if "estado" in update_data:
            update_data["estado"] = self._estado_to_string(update_data["estado"])
            if update_data["estado"] == "completado":
                update_data["fecha_completado"] = firestore.SERVER_TIMESTAMP
            else:
                update_data["fecha_completado"] = None

        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.update(update_data)

        return self.get_by_id(seguimiento_id)

    def delete(self, seguimiento_id: str) -> bool:
        doc_ref = self.db.collection("seguimientos").document(seguimiento_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True

    def delete_by_actividad(self, actividad_id: str) -> int:
        docs = (
            self.db.collection("seguimientos")
            .where("actividad_id", "==", actividad_id)
            .stream()
        )
        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1
        return count

    def delete_by_curso(self, curso_id: str) -> int:
        docs = (
            self.db.collection("seguimientos")
            .where("curso_id", "==", curso_id)
            .stream()
        )
        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1
        return count
