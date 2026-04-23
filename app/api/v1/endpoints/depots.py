from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.depot import DepotCreate, DepotUpdateStatut, DepotOut
from app.services.depot_service import DepotService

router = APIRouter(prefix="/depots", tags=["Dépôts"])


@router.get("/", response_model=list[DepotOut], summary="Lister tous les dépôts")
def list_depots(db: Session = Depends(get_db)):
    return DepotService.get_all(db)


@router.get("/{depot_id}", response_model=DepotOut, summary="Obtenir un dépôt")
def get_depot(depot_id: int, db: Session = Depends(get_db)):
    return DepotService.get_by_id(db, depot_id)


@router.post("/", response_model=DepotOut, status_code=status.HTTP_201_CREATED,
             summary="Enregistrer un dépôt de vêtement")
def create_depot(data: DepotCreate, db: Session = Depends(get_db)):
    return DepotService.create(db, data)


@router.patch("/{depot_id}/statut", response_model=DepotOut,
              summary="Mettre à jour le statut d'un dépôt")
def update_statut(depot_id: int, data: DepotUpdateStatut, db: Session = Depends(get_db)):
    return DepotService.update_statut(db, depot_id, data)
