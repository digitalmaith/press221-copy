from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date

from app.models.depot import StatutDepot


class DepotCreate(BaseModel):
    client_id: int
    employe_id: int
    service_id: int
    description: str
    date_depot: date

    @field_validator("description")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("La description ne peut pas être vide.")
        return v.strip()

    @field_validator("date_depot")
    @classmethod
    def date_depot_valide(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La date de dépôt ne peut pas être dans le futur.")
        return v


class DepotUpdateStatut(BaseModel):
    statut: StatutDepot


class DepotOut(BaseModel):
    id: int
    client_id: int
    employe_id: int
    service_id: int
    description: str
    date_depot: date
    date_retrait_prevue: date
    statut: StatutDepot

    model_config = {"from_attributes": True}
