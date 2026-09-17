from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# 1. 공통 속성을 담은 Base 스키마
class MaterialBase(BaseModel):
    name: str = Field(..., description="원자재 이름 (예: 700ml 공병)")
    category: str = Field(..., description="카테고리 (SPIRIT, BOTTLE, CAP, LABEL 등)")
    unit: str = Field(..., description="단위 (L, pcs 등)")


# 2. 생성(Create) 요청 시 필요한 스키마
class MaterialCreate(MaterialBase):
    current_stock: float = Field(default=0.0, ge=0, description="초기 재고량 (0 이상)")


# 3. 수정(Update) 요청 시 필요한 스키마 (모든 필드 선택 사항)
class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    current_stock: Optional[float] = Field(default=None, ge=0)


# 4. 클라이언트에 응답(Response)할 때 나가는 스키마
class MaterialResponse(MaterialBase):
    id: int
    current_stock: float

    # SQLAlchemy ORM 모델 객체를 Pydantic 객체로 자동 변환 허용
    model_config = ConfigDict(from_attributes=True)