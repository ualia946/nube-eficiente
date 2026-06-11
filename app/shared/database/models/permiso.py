import uuid
from sqlalchemy import ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database.base import Base 

class Permiso(Base):
    __tablename__ = "permisos"

    id_usuario: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuario.id"),
        primary_key=True
    )

    id_ambito_nodo: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ambito_nodo.id"),
        primary_key=True
    )

    rol: Mapped[str] = mapped_column(
        SAEnum("propietario", "lector", "facturacion", name = "rol_enum"),
        nullable=False
    )


    usuario: Mapped["Usuario"] = relationship(back_populates="permisos")
    ambito_nodo: Mapped["AmbitoNodo"] = relationship(back_populates="permisos")
