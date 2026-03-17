from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    title: str
    bio: Optional[str] = None
    skills: str
    match_threshold: float = 70.0
    phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True
