from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StockLogBase(BaseModel):
    target_type: str = Field(..., description="대상 유형 (MATERIAL 또는 PRODUCT)")
    target_id: str = Field(..., description="대상 원자재(int) 또는 완제품(UUID) ID 문자열")
    change_type: str = Field(..., description="변동 유형 (INBOUND, OUTBOUND, PRODUCTION, ADJUSTMENT)")
    quantity_change: float = Field(..., description="변동 수량 (+100, -0.7 등)")
    reason: Optional[str] = Field(None, description="변동 사유 및 비고")


class StockLogCreate(StockLogBase):
    pass


class StockLogResponse(StockLogBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)