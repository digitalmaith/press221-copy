from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


class StatutDepot(str, enum.Enum):
    DEPOSE = "DEPOSE"
    EN_TRAITEMENT = "EN_TRAITEMENT"
    PRET = "PRET"
    RETIRE = "RETIRE"


class Depot(Base):
    __tablename__ = "depots"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    employe_id = Column(Integer, ForeignKey("employes.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("types_service.id"), nullable=False)
    description = Column(String(500), nullable=False)
    date_depot = Column(Date, nullable=False)
    date_retrait_prevue = Column(Date, nullable=False)
    statut = Column(SAEnum(StatutDepot), nullable=False, default=StatutDepot.DEPOSE)

    client = relationship("Client", back_populates="depots")
    employe = relationship("Employe", back_populates="depots")
    service = relationship("TypeService", back_populates="depots")
