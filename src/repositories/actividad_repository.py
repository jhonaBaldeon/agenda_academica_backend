from datetime import datetime
from typing import List, Optional
from ..schemas.actividad_schema import (
    Actividad,
    ActividadCreate,
    ActividadUpdate,
    EstadoActividad,
    PrioridadActividad,
)
from ..firebase_config import get_db
from google.cloud import firestore


class ActividadRepository:
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

    def _prioridad_from_string(self, value: str) -> PrioridadActividad:
        if value == "alta":
            return PrioridadActividad.alta
        elif value == "baja":
            return PrioridadActividad.baja
        return PrioridadActividad.media

    def _prioridad_to_string(self, prioridad: PrioridadActividad) -> str:
        if prioridad == PrioridadActividad.alta:
            return "alta"
        elif prioridad == PrioridadActividad.baja:
            return "baja"
        return "media"

    def _estado_from_string(self, value: str) -> EstadoActividad:
        if value == "completado":
            return EstadoActividad.completado
        elif value == "noRealizado":
            return EstadoActividad.no_realizado
        return EstadoActividad.incompleto

    def _estado_to_string(self, estado: EstadoActividad) -> str:
        if estado == EstadoActividad.completado:
            return "completado"
        elif estado == EstadoActividad.no_realizado:
            return "noRealizado"
        return "incompleto"

    def create(self, actividad: ActividadCreate) -> Actividad:
        doc_ref = self.db.collection("actividades").document()
        now = datetime.now()

        nueva_actividad = Actividad(
            id=doc_ref.id,
            curso_id=actividad.curso_id,
            titulo=actividad.titulo,
            descripcion=actividad.descripcion,
            fecha_entrega=actividad.fecha_entrega,
            prioridad=actividad.prioridad,
            estado=EstadoActividad.incompleto,
            created_at=now,
        )

        doc_ref.set(
            {
                "curso_id": nueva_actividad.curso_id,
                "titulo": nueva_actividad.titulo,
                "descripcion": nueva_actividad.descripcion,
                "fecha_entrega": firestore.SERVER_TIMESTAMP,
                "prioridad": self._prioridad_to_string(nueva_actividad.prioridad),
                "estado": self._estado_to_string(nueva_actividad.estado),
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )

        return nueva_actividad

    def get_all(self) -> List[Actividad]:
        docs = self.db.collection("actividades").stream()
        actividades = []
        for doc in docs:
            data = doc.to_dict()
            actividades.append(
                Actividad(
                    id=doc.id,
                    curso_id=data.get("curso_id", ""),
                    titulo=data.get("titulo", ""),
                    descripcion=data.get("descripcion", ""),
                    fecha_entrega=self._parse_fecha(data.get("fecha_entrega")),
                    prioridad=self._prioridad_from_string(
                        data.get("prioridad", "media")
                    ),
                    estado=self._estado_from_string(data.get("estado", "incompleto")),
                    created_at=self._parse_fecha(data.get("created_at")),
                )
            )
        return sorted(actividades, key=lambda x: x.created_at, reverse=True)

    def get_by_id(self, actividad_id: str) -> Optional[Actividad]:
        doc = self.db.collection("actividades").document(actividad_id).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        return Actividad(
            id=doc.id,
            curso_id=data.get("curso_id", ""),
            titulo=data.get("titulo", ""),
            descripcion=data.get("descripcion", ""),
            fecha_entrega=self._parse_fecha(data.get("fecha_entrega")),
            prioridad=self._prioridad_from_string(data.get("prioridad", "media")),
            estado=self._estado_from_string(data.get("estado", "incompleto")),
            created_at=self._parse_fecha(data.get("created_at")),
        )

    def get_by_curso(self, curso_id: str) -> List[Actividad]:
        docs = (
            self.db.collection("actividades").where("curso_id", "==", curso_id).stream()
        )
        actividades = []
        for doc in docs:
            data = doc.to_dict()
            actividades.append(
                Actividad(
                    id=doc.id,
                    curso_id=data.get("curso_id", ""),
                    titulo=data.get("titulo", ""),
                    descripcion=data.get("descripcion", ""),
                    fecha_entrega=self._parse_fecha(data.get("fecha_entrega")),
                    prioridad=self._prioridad_from_string(
                        data.get("prioridad", "media")
                    ),
                    estado=self._estado_from_string(data.get("estado", "incompleto")),
                    created_at=self._parse_fecha(data.get("created_at")),
                )
            )
        return sorted(actividades, key=lambda x: x.created_at, reverse=True)

    def update(
        self, actividad_id: str, actividad_update: ActividadUpdate
    ) -> Optional[Actividad]:
        doc_ref = self.db.collection("actividades").document(actividad_id)
        if not doc_ref.get().exists:
            return None

        update_data = actividad_update.model_dump(exclude_unset=True)

        if "prioridad" in update_data:
            update_data["prioridad"] = self._prioridad_to_string(
                update_data["prioridad"]
            )
        if "estado" in update_data:
            update_data["estado"] = self._estado_to_string(update_data["estado"])
        if "fecha_entrega" in update_data:
            update_data["fecha_entrega"] = firestore.SERVER_TIMESTAMP

        update_data["updated_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.update(update_data)

        return self.get_by_id(actividad_id)

    def delete(self, actividad_id: str) -> bool:
        # Primero eliminar todos los seguimientos de la actividad
        seguimientos = (
            self.db.collection("seguimientos")
            .where("actividad_id", "==", actividad_id)
            .stream()
        )
        for seg in seguimientos:
            seg.reference.delete()

        # Luego eliminar la actividad
        doc_ref = self.db.collection("actividades").document(actividad_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True

    def delete_by_curso(self, curso_id: str) -> int:
        docs = (
            self.db.collection("actividades").where("curso_id", "==", curso_id).stream()
        )
        count = 0
        for doc in docs:
            doc.reference.delete()
            count += 1
        return count
