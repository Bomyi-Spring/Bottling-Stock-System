from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


# 1. 공통 속성을 담은 Base 스키마
class StockLogBase(BaseModel):
    target_type: str = Field(..., description="대상 유형 (MATERIAL 또는 PRODUCT)")
    target_id: int = Field(..., description="대상 원자재 또는 완제품 ID")
    change_quantity: float = Field(..., description="변동 수량 (+100, -0.7 등)")
    reason: str = Field(..., description="변동 사유 (PRODUCTION, INBOUND, DISPOSAL 등)")


# 2. 생성(Create) 요청 시 필요한 스키마
class StockLogCreate(StockLogBase):
    pass  # 로그 생성 시에는 Base 필드 그대로 사용


# 3. 클라이언트에 응답(Response)할 때 나가는 스키마
class StockLogResponse(StockLogBase):
    id: int
    created_at: datetime  # 로그 생성 일시

    model_config = ConfigDict(from_attributes=True)