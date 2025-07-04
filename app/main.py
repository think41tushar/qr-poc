from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from uuid import UUID
from app.db import create_db_and_tables, get_session
from app.models import Shop, Medicine
from app.schemas import ShopCreate, ShopRead, MedicineCreate, MedicineRead, ShopMedicinesOut

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Create a shop
@app.post("/shops", response_model=ShopRead)
def create_shop(shop: ShopCreate, session: Session = Depends(get_session)):
    db_shop = Shop(**shop.dict())
    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop


# Get shop info (+medicines)
@app.get("/shops/{shop_id}", response_model=ShopMedicinesOut)
def get_shop(shop_id: UUID, session: Session = Depends(get_session)):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    medicines = session.exec(
        select(Medicine).where(Medicine.shop_id == shop_id)
    ).all()
    return {"shop": shop, "medicines": medicines}


# Add medicine to shop
@app.post("/shops/{shop_id}/medicines", response_model=MedicineRead)
def add_medicine(shop_id: UUID, med: MedicineCreate, session: Session = Depends(get_session)):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    db_med = Medicine(**med.dict(), shop_id=shop_id)
    session.add(db_med)
    session.commit()
    session.refresh(db_med)
    return db_med