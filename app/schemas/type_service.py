from pydantic import BaseModel, field_validator
from typing import Optional


class TypeServiceBase(BaseModel):
    code: str
    libelle: str
    prix: float
    delai: int  # heures

    @field_validator("libelle", "code")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Ce champ ne peut pas être vide.")
        return v.strip()

    @field_validator("prix")
    @classmethod
    def prix_positif(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Le prix doit être supérieur à 0.")
        return v

    @field_validator("delai")
    @classmethod
    def delai_positif(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Le délai doit être un entier supérieur à 0.")
        return v


class TypeServiceCreate(TypeServiceBase):
    pass


class TypeServiceUpdate(BaseModel):
    libelle: Optional[str] = None
    prix: Optional[float] = None
    delai: Optional[int] = None


class TypeServiceOut(TypeServiceBase):
    id: int

    model_config = {"from_attributes": True}
