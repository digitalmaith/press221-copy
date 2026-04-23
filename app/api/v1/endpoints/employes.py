from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.employe import EmployeCreate, EmployeUpdate, EmployeOut
from app.services.employe_service import EmployeService

router = APIRouter(prefix="/employes", tags=["Employés"])


@router.get("/", response_model=list[EmployeOut], summary="Lister tous les employés")
def list_employes(db: Session = Depends(get_db)):
    return EmployeService.get_all(db)


@router.get("/{employe_id}", response_model=EmployeOut, summary="Obtenir un employé")
def get_employe(employe_id: int, db: Session = Depends(get_db)):
    return EmployeService.get_by_id(db, employe_id)


@router.post("/", response_model=EmployeOut, status_code=status.HTTP_201_CREATED,
             summary="Créer un employé")
def create_employe(data: EmployeCreate, db: Session = Depends(get_db)):
    return EmployeService.create(db, data)


@router.put("/{employe_id}", response_model=EmployeOut, summary="Modifier un employé")
def update_employe(employe_id: int, data: EmployeUpdate, db: Session = Depends(get_db)):
    return EmployeService.update(db, employe_id, data)


@router.delete("/{employe_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un employé")
def delete_employe(employe_id: int, db: Session = Depends(get_db)):
    EmployeService.delete(db, employe_id)
