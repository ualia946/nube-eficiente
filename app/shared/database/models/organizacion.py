import uuid
from sqlalchemy import String, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.shared.database.base import Base

class Organizacion(Base):
    """Tenant raíz de la plataforma. Agrupa usuarios y cuentas cloud bajo un mismo plan de suscripción."""

    __tablename__ = "organizacion"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default = uuid.uuid4
    )

    nombre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    plan: Mapped[str] = mapped_column(
        SAEnum("free", "pro", "enterprise", name = "plan_enum"),
        nullable=False,
        default="free"
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

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="organizacion")
    cuentas_nubes: Mapped[list["CuentaNube"]] = relationship(back_populates="organizacion")