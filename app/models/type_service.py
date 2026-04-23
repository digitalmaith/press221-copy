from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class TypeService(Base):
    __tablename__ = "types_service"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    libelle = Column(String(150), nullable=False)
    prix = Column(Float, nullable=False)
    delai = Column(Integer, nullable=False)  # en heures

    depots = relationship("Depot", back_populates="service")
