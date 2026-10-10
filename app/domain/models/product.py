from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    """완제품 도메인 엔티티"""
    id: Optional[int] = None
    name: str
    sku: str
    category: str
    unit_price: float = 0.0

    class Config:
        from_attributes = True