from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.employe import Employe
from app.models.depot import Depot, StatutDepot
from app.schemas.employe import EmployeCreate, EmployeUpdate


class EmployeService:

    @staticmethod
    def get_all(db: Session) -> list[Employe]:
        return db.query(Employe).all()

    @staticmethod
    def get_by_id(db: Session, employe_id: int) -> Employe:
        employe = db.query(Employe).filter(Employe.id == employe_id).first()
        if not employe:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employé #{employe_id} introuvable.")
        return employe

    @staticmethod
    def create(db: Session, data: EmployeCreate) -> Employe:
        # Unicité email
        if db.query(Employe).filter(Employe.email == data.email).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"L'email '{data.email}' est déjà utilisé.")
        employe = Employe(**data.model_dump())
        db.add(employe)
        db.commit()
        db.refresh(employe)
        return employe

    @staticmethod
    def update(db: Session, employe_id: int, data: EmployeUpdate) -> Employe:
        employe = EmployeService.get_by_id(db, employe_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(employe, field, value)
        db.commit()
        db.refresh(employe)
        return employe

    @staticmethod
    def delete(db: Session, employe_id: int) -> None:
        employe = EmployeService.get_by_id(db, employe_id)
        # Interdire suppression si dépôts en cours
        statuts_actifs = [StatutDepot.DEPOSE, StatutDepot.EN_TRAITEMENT, StatutDepot.PRET]
        depots_en_cours = (db.query(Depot)
                           .filter(Depot.employe_id == employe_id,
                                   Depot.statut.in_(statuts_actifs))
                           .count())
        if depots_en_cours > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Impossible de supprimer : l'employé a {depots_en_cours} dépôt(s) en cours."
            )
        db.delete(employe)
        db.commit()
