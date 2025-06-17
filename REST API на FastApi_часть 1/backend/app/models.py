from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdvertisementBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementUpdate(AdvertisementBase):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None

class Advertisement(AdvertisementBase):
    id: int
    created_at: datetime