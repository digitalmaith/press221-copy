from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.client import Client
from app.models.depot import Depot, StatutDepot
from app.schemas.client import ClientCreate, ClientUpdate


class ClientService:

    @staticmethod
    def get_all(db: Session) -> list[Client]:
        return db.query(Client).all()

    @staticmethod
    def get_by_id(db: Session, client_id: int) -> Client:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Client #{client_id} introuvable.")
        return client

    @staticmethod
    def create(db: Session, data: ClientCreate) -> Client:
        if db.query(Client).filter(Client.email == data.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"L'email '{data.email}' est déjà utilisé.")
        client = Client(**data.model_dump())
        db.add(client)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def update(db: Session, client_id: int, data: ClientUpdate) -> Client:
        client = ClientService.get_by_id(db, client_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(client, field, value)
        db.commit()
        db.refresh(client)
        return client

    @staticmethod
    def delete(db: Session, client_id: int) -> None:
        client = ClientService.get_by_id(db, client_id)
        # Interdire suppression si dépôts non retirés
        statuts_actifs = [StatutDepot.DEPOSE, StatutDepot.EN_TRAITEMENT, StatutDepot.PRET]
        depots_non_retires = (db.query(Depot)
                              .filter(Depot.client_id == client_id,
                                      Depot.statut.in_(statuts_actifs))
                              .count())
        if depots_non_retires > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Impossible de supprimer : le client a {depots_non_retires} dépôt(s) non retiré(s)."
            )
        db.delete(client)
        db.commit()
