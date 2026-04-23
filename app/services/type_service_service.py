from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.type_service import TypeService
from app.models.depot import Depot
from app.schemas.type_service import TypeServiceCreate, TypeServiceUpdate


class TypeServiceService:

    @staticmethod
    def get_all(db: Session) -> list[TypeService]:
        return db.query(TypeService).all()

    @staticmethod
    def get_by_id(db: Session, service_id: int) -> TypeService:
        service = db.query(TypeService).filter(TypeService.id == service_id).first()
        if not service:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Type de service #{service_id} introuvable.")
        return service

    @staticmethod
    def create(db: Session, data: TypeServiceCreate) -> TypeService:
        if db.query(TypeService).filter(TypeService.code == data.code).first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Le code '{data.code}' est déjà utilisé.")
        service = TypeService(**data.model_dump())
        db.add(service)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def update(db: Session, service_id: int, data: TypeServiceUpdate) -> TypeService:
        service = TypeServiceService.get_by_id(db, service_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(service, field, value)
        db.commit()
        db.refresh(service)
        return service

    @staticmethod
    def delete(db: Session, service_id: int) -> None:
        service = TypeServiceService.get_by_id(db, service_id)
        # Interdire suppression si des dépôts existent
        nb_depots = db.query(Depot).filter(Depot.service_id == service_id).count()
        if nb_depots > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Impossible de supprimer : {nb_depots} dépôt(s) utilisent ce service."
            )
        db.delete(service)
        db.commit()
