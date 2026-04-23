from sqlalchemy import Column, Integer, String, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


class PosteEnum(str, enum.Enum):
    repasseur = "repasseur"
    nettoyeur = "nettoyeur"
    accueil = "accueil"


class Employe(Base):
    __tablename__ = "employes"

    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String(100), nullable=False)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    telephone = Column(String(20))
    poste = Column(SAEnum(PosteEnum), nullable=False)

    depots = relationship("Depot", back_populates="employe")
