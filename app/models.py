from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
import uuid
from datetime import datetime, date

if TYPE_CHECKING:
    from .models import Shop

class MedicineBase(SQLModel):
    name: str
    batch: str
    expiry: date
    quantity: int

class Medicine(MedicineBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    shop_id: uuid.UUID = Field(foreign_key="shop.id")
    shop: Optional["Shop"] = Relationship(back_populates="medicines")

class ShopBase(SQLModel):
    name: str
    address: str
    phone: str

class Shop(ShopBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    medicines: List[Medicine] = Relationship(back_populates="shop")