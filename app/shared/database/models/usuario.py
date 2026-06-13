import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Enum as SAEnum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.shared.database.base import Base

class Usuario(Base):
    """Usuario autenticado perteneciente a una organización. El acceso a scopes concretos se controla mediante Permiso."""

    __tablename__ = "usuario"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    id_organizacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizacion.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str | None] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    es_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    estado: Mapped[str] = mapped_column(
        SAEnum("activo", "inactivo", name="estado_usuario_enum"),
        nullable=False,
        default="activo"
    )
    ultimo_acceso: Mapped[datetime | None] = mapped_column(nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    organizacion: Mapped["Organizacion"] = relationship(back_populates="usuarios")
    permisos: Mapped[list["Permiso"]] = relationship(back_populates="usuario")