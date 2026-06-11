from decimal import Decimal
from sqlalchemy import Enum as SAEnum, ForeignKey ,func, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from app.shared.database.base import Base

class RegistroCoste(Base):
    __tablename__ = "registro_coste"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    id_recurso: Mapped[int] = mapped_column(
        ForeignKey("recurso.id"),
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        nullable=False,
    )

    coste: Mapped[Decimal] = mapped_column(
        Numeric(precision=16, scale = 6),
        nullable=False,
    )

    moneda: Mapped[str] = mapped_column(
        SAEnum("EUR", "USD", name = "moneda_enum")
    )

    fecha_creacion: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=func.now()
    )

    recurso: Mapped["Recurso"] = relationship(back_populates="registros_costes")