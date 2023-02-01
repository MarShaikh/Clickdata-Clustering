from typing import List, Optional
from pydantic import BaseModel


class Coordinates(BaseModel):
    x: float
    y: float


class NewClickRequest(BaseModel):
    coordinates: Coordinates
    page_uuid: str


class NewClickResponse(BaseModel):
    cluster_idx: int
    is_new: bool


class PredictClickResponse(BaseModel):
    cluster_idx: Optional[int]

