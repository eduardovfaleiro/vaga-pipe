from pydantic import BaseModel
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str

class Job(JobBase):
    id: int
    posted_at: datetime

    class Config:
        from_attributes = True
