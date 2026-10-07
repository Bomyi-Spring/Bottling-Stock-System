from datetime import datetime
from sqlalchemy import String, Float, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.models.material import Material


class MaterialORM(Base):
    """
    원자재(Material) SQLAlchemy ORM 모델 (PostgreSQL 'materials' 테이블 매핑)
    """

    __tablename__ = "materials"
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    current_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    safety_stock: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def to_domain(self) -> Material:
        """
        ORM 객체를 순수 도메인 모델(Material)로 변환합니다.
        (인프라 계층의 기술적 객체를 도메인 영역으로 올릴 때 사용)
        """
        return Material(
            id=self.id,
            code=self.code,
            name=self.name,
            category=self.category,
            current_stock=self.current_stock,
            safety_stock=self.safety_stock,
            unit=self.unit,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, domain: Material) -> "MaterialORM":
        """
        순수 도메인 모델(Material)을 ORM 객체로 변환합니다.
        (도메인 객체를 DB에 저장할 때 사용)
        """
        return cls(
            id=domain.id,
            code=domain.code,
            name=domain.name,
            category=domain.category,
            current_stock=domain.current_stock,
            safety_stock=domain.safety_stock,
            unit=domain.unit,
            created_at=domain.created_at or datetime.utcnow(),
            updated_at=domain.updated_at or datetime.utcnow(),
        )