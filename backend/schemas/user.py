from pydantic import BaseModel
from typing import Optional, List
from constants import DEFAULT_MATCH_THRESHOLD

class UserBase(BaseModel):
    name: str
    email: str
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
