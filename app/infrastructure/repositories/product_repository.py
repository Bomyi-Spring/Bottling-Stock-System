from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.product import Product
from app.domain.repository_interfaces.product_repository import ProductRepositoryInterface
from app.infrastructure.models.product_model import ProductORM


class SqlAlchemyProductRepository(ProductRepositoryInterface):
    """
    SQLAlchemy 비동기 세션을 사용하는 완제품(Product) 구체 리포지토리
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        UUID 식별자로 단일 완제품을 조회합니다.
        """
        result = await self.session.get(ProductORM, product_id)
        if not result:
            return None
        return result.to_domain()

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """
        SKU 코드로 단일 완제품을 조회합니다.
        """
        stmt = select(ProductORM).where(ProductORM.sku == sku)
        result = await self.session.execute(stmt)
        orm_product = result.scalars().first()
        if not orm_product:
            return None
        return orm_product.to_domain()

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        전체 완제품 목록을 페이징 처리하여 조회합니다.
        """
        stmt = select(ProductORM).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        orm_list = result.scalars().all()
        return [orm.to_domain() for orm in orm_list]

    async def save(self, product: Product) -> Product:
        """
        완제품 도메인 객체를 DB에 저장(INSERT 또는 UPDATE)합니다.
        - JSONB 레시피 변경 사항도 함께 반영됩니다.
        """
        if product.id:
            existing_orm = await self.session.get(ProductORM, product.id)
            if existing_orm:
                existing_orm.sku = product.sku
                existing_orm.name = product.name
                existing_orm.category = product.category
                existing_orm.current_stock = product.current_stock
                existing_orm.price = product.price
                existing_orm.recipe = product.recipe  # JSONB 필드 신규 딕셔너리로 업데이트
                await self.session.flush()
                return existing_orm.to_domain()

        new_orm = ProductORM.from_domain(product)
        self.session.add(new_orm)
        await self.session.flush()
        await self.session.refresh(new_orm)
        return new_orm.to_domain()

    async def update_stock(self, product_id: UUID, quantity_change: int) -> Optional[Product]:
        """
        상품의 재고 수량을 변경합니다. (양수: 입고, 음수: 출고)
        - 행 잠금(SELECT ... FOR UPDATE)으로 동시 요청 시 재고 경합을 방지합니다.
        - 변경 후 재고가 음수가 되면 ValueError를 발생시킵니다.
        """
        stmt = (
            select(ProductORM)
            .where(ProductORM.id == product_id)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        orm_product = result.scalars().first()
        if not orm_product:
            return None

        new_stock = orm_product.current_stock + quantity_change
        if new_stock < 0:
            raise ValueError(
                f"재고가 부족합니다. (현재: {orm_product.current_stock}, 변경: {quantity_change})"
            )

        orm_product.current_stock = new_stock
        await self.session.flush()
        await self.session.refresh(orm_product)
        return orm_product.to_domain()

    async def delete(self, product_id: UUID) -> bool:
        """
        UUID로 완제품 레코드를 삭제합니다.
        """
        orm_product = await self.session.get(ProductORM, product_id)
        if not orm_product:
            return False
        await self.session.delete(orm_product)
        await self.session.flush()
        return True