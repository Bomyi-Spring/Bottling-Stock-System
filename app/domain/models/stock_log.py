from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockLog(BaseModel):
    """재고 변동 이력 도메인 엔티티"""
    id: Optional[int] = None
    material_id: Optional[int] = None
    product_id: Optional[int] = None
    change_quantity: float
    reason: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True