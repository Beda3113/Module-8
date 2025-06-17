from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database simulation
ads_db = {}

# Models
class AdBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    author: str

class AdCreate(AdBase):
    pass

class Ad(AdBase):
    id: str
    created_at: datetime

# Endpoints
@app.post("/advertisements", response_model=Ad)
def create_ad(ad: AdCreate):
    ad_id = str(uuid.uuid4())
    new_ad = Ad(
        **ad.dict(),
        id=ad_id,
        created_at=datetime.now()
    )
    ads_db[ad_id] = new_ad
    return new_ad

@app.get("/advertisements", response_model=List[Ad])
def list_ads():
    return list(ads_db.values())

@app.get("/advertisements/{ad_id}", response_model=Ad)
def get_ad(ad_id: str):
    if ad_id not in ads_db:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ads_db[ad_id]