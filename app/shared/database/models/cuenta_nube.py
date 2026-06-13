import uuid
from sqlalchemy import String, Enum as SAEnum, ForeignKey ,func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
from app.shared.database.base import Base

class CuentaNube(Base):
    """Cuenta de un proveedor cloud vinculada a una organización.

    El campo credenciales almacena en JSONB las claves de autenticación con estructura
    específica de cada proveedor (ver AzureProvider.from_credentials para el esquema Azure).
    """

    __tablename__ = "cuenta_nube"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    id_organizacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizacion.id"),
        nullable=False
    )

    proveedor: Mapped[str] = mapped_column(
        SAEnum("azure", "aws", "gcp", name = "proveedor_enum"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    credenciales: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        SAEnum("activa", "error", "desconectada", name = "estado_cuenta_enum"),
        nullable=False
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    organizacion: Mapped["Organizacion"] = relationship(back_populates="cuentas_nubes")
    ambitos_nodo: Mapped[list["AmbitoNodo"]] = relationship(back_populates="cuenta_nube")
