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

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
