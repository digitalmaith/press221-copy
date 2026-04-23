from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    telephone = Column(String(20), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    adresse = Column(String(255))

    depots = relationship("Depot", back_populates="client")
