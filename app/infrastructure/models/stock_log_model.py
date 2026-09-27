import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.domain.models.stock_log import StockLog


class StockLogORM(Base):
    """
    재고 변동 이력(StockLog) SQLAlchemy ORM 모델 (PostgreSQL 'stock_logs' 테이블 매핑)
    """

    __tablename__ = "stock_logs"

    # UUID Primary Key
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    
    # 변동 대상 구분 ("MATERIAL" 또는 "PRODUCT")
    target_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # 대상 식별자 (문자열로 저장하여 Integer ID의 Material과 UUID의 Product 모두 수용)
    target_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # 변동 유형 ("INBOUND", "OUTBOUND", "PRODUCTION", "ADJUSTMENT")
    change_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    
    # 변동 수량 (양수: 증가, 음수: 감소)
    quantity_change: Mapped[float] = mapped_column(Float, nullable=False)
    
    # 변동 사유 및 비고
    reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # 기록 생성 일시
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    def to_domain(self) -> StockLog:
        """
        ORM 객체를 순수 도메인 모델(StockLog)로 변환합니다.
        """
        return StockLog(
            id=self.id,
            target_type=self.target_type,
            target_id=self.target_id,
            change_type=self.change_type,
            quantity_change=self.quantity_change,
            reason=self.reason,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, domain: StockLog) -> "StockLogORM":
        """
        순수 도메인 모델(StockLog)을 ORM 객체로 변환합니다.
        """
        return cls(
            id=domain.id or uuid.uuid4(),
            target_type=domain.target_type,
            target_id=str(domain.target_id),  # UUID 또는 int를 문자열로 규격화하여 저장
            change_type=domain.change_type,
            quantity_change=domain.quantity_change,
            reason=domain.reason,
            created_at=domain.created_at or datetime.utcnow(),
        )