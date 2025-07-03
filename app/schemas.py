from typing import List, Optional
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel

class ShopCreate(BaseModel):
    name: str
    address: str
    phone: str

class ShopRead(BaseModel):
    id: UUID
    name: str
    address: str
    phone: str
    created_at: datetime

class MedicineCreate(BaseModel):
    name: str
    batch: str
    expiry: date
    quantity: int

class MedicineRead(BaseModel):
    id: int
    name: str
    batch: str
    expiry: date
    quantity: int

class ShopMedicinesOut(BaseModel):
    shop: ShopRead
    medicines: List[MedicineRead]