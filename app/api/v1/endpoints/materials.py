from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import get_material_service
from app.domain.exceptions import (
    DuplicateSKUException,
    InsufficientStockException,
    MaterialNotFoundException,
)
from app.services.material_service import MaterialService


# ==========================================
# Pydantic Schemas (DTOs)
# ==========================================

class MaterialCreateSchema(BaseModel):
    code: str = Field(..., example="MAT-GIN-001", description="원자재 고유 코드")
    name: str = Field(..., example="Dry Gin Base", description="원자재명")
    category: str = Field(..., example="Spirits", description="카테고리")
    current_stock: float = Field(0.0, ge=0, description="초기 재고 수량")
    safety_stock: float = Field(0.0, ge=0, description="안전 재고 수량")
    unit: str = Field(..., example="Liters", description="단위")


class MaterialStockUpdateSchema(BaseModel):
    quantity_change: float = Field(..., description="변동 수량 (양수: 입고/증가, 음수: 출고/감소)")
    reason: str = Field(..., example="정기 입고", description="변동 사유")


class MaterialResponseSchema(BaseModel):
    id: int
    code: str
    name: str
    category: str
    current_stock: float
    safety_stock: float
    unit: str

    class Config:
        from_attributes = True


# ==========================================
# Router Definition
# ==========================================

router = APIRouter()


@router.post("/", response_model=MaterialResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_material(
    payload: MaterialCreateSchema,
    service: MaterialService = Depends(get_material_service),
):
    """
    신규 원자재를 등록합니다.
    """
    try:
        # service.create_material은 개별 인자가 아닌 schema(또는 payload) 객체를 전달받습니다.
        return await service.create_material(payload)
    except DuplicateSKUException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[MaterialResponseSchema])
async def list_materials(
    skip: int = 0,
    limit: int = 100,
    service: MaterialService = Depends(get_material_service),
):
    """
    원자재 목록을 페이징하여 조회합니다.
    """
    return await service.list_materials(skip=skip, limit=limit)


@router.get("/{material_id}", response_model=MaterialResponseSchema)
async def get_material(
    material_id: int,
    service: MaterialService = Depends(get_material_service),
):
    """
    ID로 단일 원자재를 상세 조회합니다.
    """
    material = await service.get_material(material_id)
    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found",
        )
    return material


@router.patch("/{material_id}/stock", response_model=MaterialResponseSchema)
async def adjust_stock(
    material_id: int,
    payload: MaterialStockUpdateSchema,
    service: MaterialService = Depends(get_material_service),
):
    """
    원자재 재고 수량을 조정(입고/출고/차감)합니다.
    """
    try:
        updated_material = await service.adjust_stock(
            material_id=material_id,
            quantity_change=payload.quantity_change,
            reason=payload.reason,
        )
    except MaterialNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (ValueError, InsufficientStockException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not updated_material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found",
        )
    return updated_material


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(
    material_id: int,
    service: MaterialService = Depends(get_material_service),
):
    """
    원자재를 삭제합니다.
    """
    success = await service.delete_material(material_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Material with ID {material_id} not found",
        )