from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

from app.models.depot import Depot, StatutDepot
from app.models.client import Client
from app.models.employe import Employe
from app.models.type_service import TypeService
from app.schemas.depot import DepotCreate, DepotUpdateStatut


class DepotService:

    @staticmethod
    def get_all(db: Session) -> list[Depot]:
        return db.query(Depot).all()

    @staticmethod
    def get_by_id(db: Session, depot_id: int) -> Depot:
        depot = db.query(Depot).filter(Depot.id == depot_id).first()
        if not depot:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Dépôt #{depot_id} introuvable.")
        return depot

    @staticmethod
    def create(db: Session, data: DepotCreate) -> Depot:
        # Vérifier existence des entités liées
        if not db.query(Client).filter(Client.id == data.client_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Client #{data.client_id} introuvable.")

        if not db.query(Employe).filter(Employe.id == data.employe_id).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employé #{data.employe_id} introuvable.")

        service = db.query(TypeService).filter(TypeService.id == data.service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Type de service #{data.service_id} introuvable.")

        # Calculer la date de retrait prévue
        date_retrait_prevue = data.date_depot + timedelta(hours=service.delai)

        depot = Depot(
            client_id=data.client_id,
            employe_id=data.employe_id,
            service_id=data.service_id,
            description=data.description,
            date_depot=data.date_depot,
            date_retrait_prevue=date_retrait_prevue,
            statut=StatutDepot.DEPOSE,
        )
        db.add(depot)
        db.commit()
        db.refresh(depot)
        return depot

    @staticmethod
    def update_statut(db: Session, depot_id: int, data: DepotUpdateStatut) -> Depot:
        depot = DepotService.get_by_id(db, depot_id)
        depot.statut = data.statut
        db.commit()
        db.refresh(depot)
        return depot
