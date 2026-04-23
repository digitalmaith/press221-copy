from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.models.employe import PosteEnum


class EmployeBase(BaseModel):
    prenom: str
    nom: str
    email: EmailStr
    telephone: Optional[str] = None
    poste: PosteEnum

    @field_validator("prenom", "nom")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Ce champ ne peut pas être vide.")
        return v.strip()


class EmployeCreate(EmployeBase):
    pass


class EmployeUpdate(BaseModel):
    prenom: Optional[str] = None
    nom: Optional[str] = None
    telephone: Optional[str] = None
    poste: Optional[PosteEnum] = None


class EmployeOut(EmployeBase):
    id: int

    model_config = {"from_attributes": True}
