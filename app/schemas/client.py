from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class ClientBase(BaseModel):
    prenom: str
    nom: str
    telephone: str
    email: EmailStr
    adresse: Optional[str] = None

    @field_validator("prenom", "nom", "telephone")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Ce champ ne peut pas être vide.")
        return v.strip()


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    prenom: Optional[str] = None
    nom: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class ClientOut(ClientBase):
    id: int

    model_config = {"from_attributes": True}
