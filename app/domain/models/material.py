from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Material(Base):
    """원자재 테이블 (원액, 공병, 캡, 라벨 등)"""
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # SPIRIT, BOTTLE, CAP, LABEL
    current_stock = Column(Float, default=0.0)
    unit = Column(String(20), nullable=False)      # L, pcs etc.