from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    """완제품 테이블 (판매용 병입 상품)"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    current_stock = Column(Integer, default=0)

    recipe_items = relationship("RecipeItem", back_populates="product", cascade="all, delete-orphan")


class RecipeItem(Base):
    """BOM(Bill of Materials): 완제품 1개 생산에 필요한 원자재 수량"""
    __tablename__ = "recipe_items"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    required_quantity = Column(Float, nullable=False)

    product = relationship("Product", back_populates="recipe_items")
    material = relationship("Material")