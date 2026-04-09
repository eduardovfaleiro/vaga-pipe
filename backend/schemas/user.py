from pydantic import BaseModel, field_validator
from typing import Optional, List
import re
from constants import DEFAULT_MATCH_THRESHOLD

class UserBase(BaseModel):
    name: str
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("email inválido")
        return v
    title: str
    skills: List[str]
    match_threshold: float = DEFAULT_MATCH_THRESHOLD
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("senha deve ter no mínimo 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("senha deve ter no mínimo 1 letra maiúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("senha deve ter no mínimo 1 número")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("senha deve ter no mínimo 1 caractere especial")
        return v

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
