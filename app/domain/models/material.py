from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Material(BaseModel):
    """원자재 도메인 엔티티"""
    id: Optional[int] = None
    code: str
    name: str
    category: str  # SPIRIT, BOTTLE, CAP, LABEL 등
    current_stock: float = 0.0
    safety_stock: float = 0.0
    unit: str  # L, pcs 등
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True