from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from app.domain.schemas.material import MaterialResponse


# ==========================================
# 1. RecipeItem (BOM 항목) 스키마
# ==========================================

class RecipeItemBase(BaseModel):
    material_id: int = Field(..., description="사용할 원자재 ID")
    required_quantity: float = Field(..., gt=0, description="필요 수량 (0보다 커야 함)")


class RecipeItemCreate(RecipeItemBase):
    pass  # 생성 시에는 Base 필드만으로 충분함


class RecipeItemResponse(RecipeItemBase):
    id: int
    material: Optional[MaterialResponse] = None  # 원자재의 상세 정보까지 포함하여 응답

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 2. Product (완제품) 스키마
# ==========================================

class ProductBase(BaseModel):
    sku: str = Field(..., description="고유 상품 코드 (예: WHISKY-SINGLE-700)")
    name: str = Field(..., description="완제품 이름 (예: 스페셜 싱글몰트 700ml)")


class ProductCreate(ProductBase):
    current_stock: int = Field(default=0, ge=0, description="초기 완제품 재고 수량")
    recipe_items: List[RecipeItemCreate] = Field(
        default=[], 
        description="완제품 등록 시 함께 입력할 레시피 항목 목록"
    )


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    current_stock: Optional[int] = Field(default=None, ge=0)


class ProductResponse(ProductBase):
    id: int
    current_stock: int
    recipe_items: List[RecipeItemResponse] = []  # 레시피 항목 목록 포함하여 응답

    model_config = ConfigDict(from_attributes=True)