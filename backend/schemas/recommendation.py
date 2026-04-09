from pydantic import BaseModel
from typing import Literal


class RecommendationStatusUpdate(BaseModel):
    status: Literal["pending", "applied", "rejected"]
