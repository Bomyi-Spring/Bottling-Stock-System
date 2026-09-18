from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.domain.models.stock_log import StockLog
from app.domain.schemas.stock_log import StockLogCreate
from app.domain.exceptions import StockLogNotFoundException
from app.domain.repository_interfaces.stock_log_repository import StockLogRepositoryInterface


class StockLogService:
    """
    재고 변동 이력(StockLog) 기록 및 조회 비즈니스 유스케이스 서비스
    """

    def __init__(self, stock_log_repo: StockLogRepositoryInterface):
        # 의존성 주입(Dependency Injection)
        self.stock_log_repo = stock_log_repo

    async def log_change(self, schema: StockLogCreate) -> StockLog:
        """
        [이력 기록] 새로운 재고 변동 이력을 기록합니다.
        - 입고(INBOUND), 출고(OUTBOUND), 생산 소진(PRODUCTION), 재고 조정(ADJUSTMENT) 등
        """
        new_log = StockLog(
            target_type=schema.target_type,  # "MATERIAL" 또는 "PRODUCT"
            target_id=schema.target_id,      # 원자재 ID 또는 완제품 UUID
            change_type=schema.change_type,  # 변동 유형
            quantity_change=schema.quantity_change,  # 변동 수량 (양수/음수)
            reason=schema.reason,            # 사유 설명
            created_at=datetime.utcnow(),
        )
        return await self.stock_log_repo.save(new_log)

    async def get_log_by_id(self, log_id: UUID) -> StockLog:
        """
        ID로 특정 재고 변동 이력 1건을 조회합니다.
        - 존재하지 않을 경우 StockLogNotFoundException 예외를 발생시킵니다.
        """
        log = await self.stock_log_repo.get_by_id(log_id)
        if not log:
            raise StockLogNotFoundException(log_id=log_id)
        return log

    async def get_logs_by_target(
        self,
        target_type: str,
        target_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[StockLog]:
        """
        [대상별 조회] 특정 원자재나 완제품의 재고 변동 히스토리를 페이징하여 조회합니다.
        """
        return await self.stock_log_repo.list_by_target(
            target_type=target_type,
            target_id=target_id,
            skip=skip,
            limit=limit,
        )

    async def get_logs_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100,
    ) -> List[StockLog]:
        """
        [기간별 조회] 특정 기간(시작일~종료일) 동안 발생한 재고 변동 이력 리포트를 조회합니다.
        - start_date가 end_date보다 미래일 경우 ValueError 발생
        """
        if start_date > end_date:
            raise ValueError("시작일은 종료일보다 이전이어야 합니다.")

        return await self.stock_log_repo.list_by_date_range(
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit,
        )