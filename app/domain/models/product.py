from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class Product(BaseModel):
    """완제품 도메인 엔티티"""
    id: Optional[UUID] = None
    sku: str
    name: str
    category: str
    current_stock: int = 0
    price: float = 0.0
    recipe: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True