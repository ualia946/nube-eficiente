import uuid
from sqlalchemy import String, Enum as SAEnum, ForeignKey ,func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.shared.database.base import Base

class Recurso(Base):
    """Recurso cloud concreto (VM, base de datos, almacenamiento, etc.) dentro de un scope.

    recurso_ref_id es el ID nativo del proveedor; se usa como clave natural para upserts idempotentes.
    propiedades almacena metadatos adicionales específicos del proveedor en formato libre (JSONB).
    """

    __tablename__ = "recurso"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
    )

    id_ambito_nodo: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ambito_nodo.id"),
        nullable=False,
    )

    recurso_ref_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(45),
        nullable=False
    )

    ubicacion: Mapped[str] = mapped_column(
        String(45),
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        SAEnum("activo", "detenido", "eliminado", name = "tipo_enum"),
        nullable=False
    )

    propiedades: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        server_default= func.now(),
        onupdate= func.now(),
        nullable=False
    )

    ambito_nodo: Mapped["AmbitoNodo"] = relationship(back_populates="recursos")
    registros_costes: Mapped[list["RegistroCoste"]] = relationship(back_populates="recurso")
    anomalias: Mapped[list["Anomalia"]] = relationship(back_populates="recurso")
    

