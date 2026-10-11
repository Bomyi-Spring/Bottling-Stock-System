from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class StockLog(BaseModel):
    """재고 변동 이력 도메인 엔티티"""
    id: Optional[UUID] = None
    target_type: str            # "MATERIAL" 또는 "PRODUCT"
    target_id: str              # 원자재 int ID / 완제품 UUID를 문자열로 저장
    change_type: str            # INBOUND, OUTBOUND, PRODUCTION, ADJUSTMENT
    quantity_change: float      # 양수: 증가, 음수: 감소
    reason: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True