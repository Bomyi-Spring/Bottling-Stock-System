from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.deps import get_stock_log_service
from app.services.stock_log_service import StockLogService


# ==========================================
# Pydantic Schemas (DTOs)
# ==========================================

class StockLogResponseSchema(BaseModel):
    id: UUID
    target_type: str = Field(..., example="MATERIAL", description="변동 대상 구분 (MATERIAL / PRODUCT)")
    target_id: str = Field(..., example="1", description="대상 식별자 (Material ID 또는 Product UUID)")
    change_type: str = Field(..., example="INBOUND", description="변동 유형 (INBOUND / OUTBOUND / PRODUCTION 등)")
    quantity_change: float = Field(..., example=10.0, description="변동 수량")
    reason: Optional[str] = Field(None, example="정기 입고", description="변동 사유")
    created_at: datetime

    class Config:
        from_attributes = True


# ==========================================
# Router Definition
# ==========================================

router = APIRouter()


@router.get("/", response_model=List[StockLogResponseSchema])
async def list_stock_logs(
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(100, ge=1, le=500, description="조회할 최대 레코드 수"),
    service: StockLogService = Depends(get_stock_log_service),
):
    """
    전체 재고 변동 감사(Audit) 로그를 최신순으로 페이징 조회합니다.
    """
    return await service.list_all_logs(skip=skip, limit=limit)


@router.get("/target/{target_type}/{target_id}", response_model=List[StockLogResponseSchema])
async def list_stock_logs_by_target(
    target_type: str,
    target_id: str,
    skip: int = Query(0, ge=0, description="건너뛸 레코드 수"),
    limit: int = Query(100, ge=1, le=500, description="조회할 최대 레코드 수"),
    service: StockLogService = Depends(get_stock_log_service),
):
    """
    특정 대상(MATERIAL / PRODUCT) 및 대상 ID 기준 변동 이력을 최신순으로 조회합니다.
    - target_type 예시: 'MATERIAL', 'PRODUCT'
    - target_id 예시: Material ID '1' 또는 Product UUID '550e8400-e29b-41d4-a716-446655440000'
    """
    normalized_target_type = target_type.upper()
    if normalized_target_type not in ["MATERIAL", "PRODUCT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="target_type must be either 'MATERIAL' or 'PRODUCT'",
        )

    return await service.list_logs_by_target(
        target_type=normalized_target_type,
        target_id=target_id,
        skip=skip,
        limit=limit,
    )