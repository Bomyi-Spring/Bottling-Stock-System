from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.stock_log import StockLog
from app.domain.repository_interfaces.stock_log_repository import StockLogRepositoryInterface
from app.infrastructure.models.stock_log_model import StockLogORM


class SqlAlchemyStockLogRepository(StockLogRepositoryInterface):
    """
    SQLAlchemy 비동기 세션을 사용하는 재고 변동 이력(StockLog) 구체 리포지토리
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, log_id: UUID) -> Optional[StockLog]:
        """
        UUID로 단일 재고 변동 로그를 조회합니다.
        """
        result = await self.session.get(StockLogORM, log_id)
        if not result:
            return None
        return result.to_domain()

    async def save(self, stock_log: StockLog) -> StockLog:
        """
        재고 변동 로그를 DB에 새로 기록(INSERT)합니다.
        (로그는 수정되지 않고 추가만 되는 Append-only 데이터입니다)
        """
        new_orm = StockLogORM.from_domain(stock_log)
        self.session.add(new_orm)
        await self.session.flush()
        await self.session.refresh(new_orm)
        return new_orm.to_domain()

    async def list_by_target(
        self, target_type: str, target_id: str, skip: int = 0, limit: int = 100
    ) -> List[StockLog]:
        """
        특정 대상(원자재 MATERIAL / 완제품 PRODUCT) 및 대상 ID 기준 최근 순 변동 이력을 조회합니다.
        """
        stmt = (
            select(StockLogORM)
            .where(
                StockLogORM.target_type == target_type,
                StockLogORM.target_id == str(target_id),
            )
            .order_by(StockLogORM.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        orm_list = result.scalars().all()
        return [orm.to_domain() for orm in orm_list]

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[StockLog]:
        """
        전체 재고 변동 로그 목록을 최신순으로 조회합니다.
        """
        stmt = (
            select(StockLogORM)
            .order_by(StockLogORM.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        orm_list = result.scalars().all()
        return [orm.to_domain() for orm in orm_list]