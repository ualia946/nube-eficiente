import uuid
from sqlalchemy import String, ForeignKey ,func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from app.shared.database.base import Base

class AmbitoNodo(Base):
    __tablename__ = "ambito_nodo"

    # ATRIBUTOS

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    id_cuenta_nube: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cuenta_nube.id"),
        nullable=False
    )

    padre_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ambito_nodo.id"),
        nullable=True
    )

    tipo_nodo: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    proveedor_ref_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # RELACIONES

    cuenta_nube: Mapped["CuentaNube"] = relationship(back_populates="ambitos_nodo")
    padre: Mapped[Optional["AmbitoNodo"]] = relationship(
        back_populates="hijos",
        remote_side="AmbitoNodo.id"
    )
    hijos: Mapped[list["AmbitoNodo"]] = relationship(back_populates="padre")
    recursos: Mapped[list["Recurso"]] = relationship(back_populates="ambito_nodo")
    permisos: Mapped[list["Permiso"]] = relationship(back_populates="ambito_nodo")