import uuid
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, Float, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.models.product import Product


class ProductORM(Base):
    """
    완제품(Product) SQLAlchemy ORM 모델 (PostgreSQL 'products' 테이블 매핑)
    """

    __tablename__ = "products"

    # UUID Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    current_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    price: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    
    # 레시피(BOM) 데이터를 JSONB 구조로 저장 (예: {"material_id_1": 1.5, "material_id_2": 2.0})
    recipe: Mapped[Dict[str, Any]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=False, default=dict
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_domain(self) -> Product:
        """
        ORM 객체를 순수 도메인 모델(Product)로 변환합니다.
        """
        return Product(
            id=self.id,
            sku=self.sku,
            name=self.name,
            category=self.category,
            current_stock=self.current_stock,
            price=self.price,
            recipe=self.recipe,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, domain: Product) -> "ProductORM":
        """
        순수 도메인 모델(Product)을 ORM 객체로 변환합니다.
        """
        return cls(
            id=domain.id or uuid.uuid4(),
            sku=domain.sku,
            name=domain.name,
            category=domain.category,
            current_stock=domain.current_stock,
            price=domain.price,
            recipe=domain.recipe,
            created_at=domain.created_at or datetime.utcnow(),
            updated_at=domain.updated_at or datetime.utcnow(),
        )