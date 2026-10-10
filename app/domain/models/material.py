from pydantic import BaseModel
from typing import Optional

class Material(BaseModel):
    """원자재 도메인 엔티티"""
    id: Optional[int] = None
    name: str
    category: str  # SPIRIT, BOTTLE, CAP, LABEL 등
    current_stock: float = 0.0
    unit: str  # L, pcs 등

    class Config:
        from_attributes = True