from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import get_product_service
from app.domain.exceptions import (
    DuplicateSKUException,
    InsufficientStockException,
    MaterialNotFoundException,
    ProductNotFoundException,
)
from app.services.product_service import ProductService


# ==========================================
# Pydantic Schemas (DTOs)
# ==========================================

class ProductCreateSchema(BaseModel):
    sku: str = Field(..., example="PRD-GIN-700ML", description="완제품 고유 SKU")
    name: str = Field(..., example="London Dry Gin 700ml", description="완제품명")
    category: str = Field(..., example="Gin", description="카테고리")
    current_stock: int = Field(0, ge=0, description="초기 완제품 재고 수량")
    price: float = Field(0.0, ge=0, description="판매 단가")
    recipe: Dict[str, float] = Field(
        ...,
        example={"1": 0.7, "2": 1.0},
        description="원자재 조합 레시피 (key: material_id 문자열, value: 필요 소모량)"
    )


class ProduceRequestSchema(BaseModel):
    quantity: int = Field(..., gt=0, description="생산할 완제품 수량 (1개 이상)")


class ProductResponseSchema(BaseModel):
    id: UUID
    sku: str
    name: str
    category: str
    current_stock: int
    price: float
    recipe: Dict[str, Any]

    class Config:
        from_attributes = True


# ==========================================
# Router Definition
# ==========================================

router = APIRouter()


@router.post("/", response_model=ProductResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateSchema,
    service: ProductService = Depends(get_product_service),
):
    """
    신규 완제품 및 BOM(레시피) 정보를 등록합니다.
    """
    try:
        return await service.create_product(payload)
    except DuplicateSKUException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ProductResponseSchema])
async def list_products(
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    """
    완제품 목록을 페이징하여 조회합니다.
    """
    return await service.get_all_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductResponseSchema)
async def get_product(
    product_id: UUID,
    service: ProductService = Depends(get_product_service),
):
    """
    UUID로 단일 완제품을 상세 조회합니다.
    """
    try:
        return await service.get_product_by_id(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{product_id}/produce", response_model=ProductResponseSchema)
async def produce_product(
    product_id: UUID,
    payload: ProduceRequestSchema,
    service: ProductService = Depends(get_product_service),
):
    """
    완제품 보틀링 생산을 실행합니다.
    - 레시피 비율에 따라 필요한 원자재 재고 수량을 자동으로 검증 및 차감합니다.
    - 완제품 재고 수량을 증가시킵니다.
    """
    try:
        return await service.produce_product(
            product_id=product_id,
            quantity=payload.quantity,
        )
    except ProductNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (MaterialNotFoundException, InsufficientStockException, ValueError) as e:
        # 원자재 재고 부족 또는 존재하지 않는 원자재 ID
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))