from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.type_service import TypeServiceCreate, TypeServiceUpdate, TypeServiceOut
from app.services.type_service_service import TypeServiceService

router = APIRouter(prefix="/services", tags=["Types de service"])


@router.get("/", response_model=list[TypeServiceOut], summary="Lister tous les types de service")
def list_services(db: Session = Depends(get_db)):
    return TypeServiceService.get_all(db)


@router.get("/{service_id}", response_model=TypeServiceOut, summary="Obtenir un type de service")
def get_service(service_id: int, db: Session = Depends(get_db)):
    return TypeServiceService.get_by_id(db, service_id)


@router.post("/", response_model=TypeServiceOut, status_code=status.HTTP_201_CREATED,
             summary="Créer un type de service")
def create_service(data: TypeServiceCreate, db: Session = Depends(get_db)):
    return TypeServiceService.create(db, data)


@router.put("/{service_id}", response_model=TypeServiceOut, summary="Modifier un type de service")
def update_service(service_id: int, data: TypeServiceUpdate, db: Session = Depends(get_db)):
    return TypeServiceService.update(db, service_id, data)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un type de service")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    TypeServiceService.delete(db, service_id)
