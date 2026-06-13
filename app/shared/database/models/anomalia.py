from decimal import Decimal
from sqlalchemy import String, Enum as SAEnum, ForeignKey ,func, Integer, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.shared.database.base import Base

class Anomalia(Base):
    """Anomalía de coste detectada sobre un recurso. Recoge severidad, descripción del problema y ahorro estimado."""

    __tablename__ = "anomalia"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    id_recurso: Mapped[int] = mapped_column(
        ForeignKey("recurso.id"),
        nullable=False
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    severidad: Mapped[str] = mapped_column(
        SAEnum("info", "warning", "high", "critical", name="severidad_enum"),
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    solucion: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    ahorro_estimado: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=4),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        SAEnum("activa", "resuelta", "ignorada", name = "estado_anomalia_enum"),
        nullable=True,
        default="activa"
    )

    detectada_en: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )

    fecha_actualizacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    recurso: Mapped["Recurso"] = relationship(back_populates="anomalias")



