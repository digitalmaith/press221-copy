from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientOut
from app.services.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientOut], summary="Lister tous les clients")
def list_clients(db: Session = Depends(get_db)):
    return ClientService.get_all(db)


@router.get("/{client_id}", response_model=ClientOut, summary="Obtenir un client")
def get_client(client_id: int, db: Session = Depends(get_db)):
    return ClientService.get_by_id(db, client_id)


@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED,
             summary="Créer un client")
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    return ClientService.create(db, data)


@router.put("/{client_id}", response_model=ClientOut, summary="Modifier un client")
def update_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db)):
    return ClientService.update(db, client_id, data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Supprimer un client")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    ClientService.delete(db, client_id)
