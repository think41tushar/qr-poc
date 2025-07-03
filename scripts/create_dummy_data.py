import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session
from app.db import engine, create_db_and_tables
from app.models import Shop, Medicine
from datetime import date
import uuid

def create_dummy_data():
    create_db_and_tables()  # Ensures tables exist

    with Session(engine) as session:
        # ---- Create shops ----
        shop1 = Shop(
            name="Tushar Medicos",
            address="123 Main Street",
            phone="1234567890"
        )
        shop2 = Shop(
            name="Central Drugs",
            address="456 Side Road",
            phone="9876543210"
        )
        session.add(shop1)
        session.add(shop2)
        session.commit()
        session.refresh(shop1)
        session.refresh(shop2)

        # ---- Create medicines ----
        med1 = Medicine(
            shop_id=shop1.id,
            name="Paracetamol",
            batch="ABC123",
            expiry=date(2025, 12, 31),
            quantity=50,
        )
        med2 = Medicine(
            shop_id=shop1.id,
            name="Ibuprofen",
            batch="XYZ987",
            expiry=date(2024, 11, 30),
            quantity=30,
        )
        med3 = Medicine(
            shop_id=shop2.id,
            name="Amoxicillin",
            batch="AMO2025",
            expiry=date(2026, 5, 20),
            quantity=100,
        )

        session.add(med1)
        session.add(med2)
        session.add(med3)
        session.commit()
        print("Dummy data created!")

if __name__ == "__main__":
    create_dummy_data()