from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class StockLog(Base):
    """재고 변동 이력 추적 테이블"""
    __tablename__ = "stock_logs"

    id = Column(Integer, primary_key=True, index=True)
    target_type = Column(String(20), nullable=False)  # "MATERIAL" 또는 "PRODUCT"
    target_id = Column(Integer, nullable=False)       # 해당 원자재 또는 완제품 ID
    change_quantity = Column(Float, nullable=False)   # 변동량
    reason = Column(String(50), nullable=False)       # "PRODUCTION", "INBOUND" 등
    created_at = Column(DateTime(timezone=True), server_default=func.now())