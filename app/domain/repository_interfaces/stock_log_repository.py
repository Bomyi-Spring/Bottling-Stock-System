from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.domain.entities.stock_log import StockLog


class StockLogRepositoryInterface(ABC):
    """
    재고 변동 이력(StockLog) 도메인 엔티티를 관리하기 위한 추상 리포지토리 인터페이스
    """

    @abstractmethod
    async def save(self, stock_log: StockLog) -> StockLog:
        """
        새로운 재고 변동 이력을 기록(저장)합니다.
        """
        pass

    @abstractmethod
    async def get_by_id(self, log_id: UUID) -> Optional[StockLog]:
        """
        ID로 특정 재고 이력 건을 조회합니다.
        """
        pass

    @abstractmethod
    async def list_by_target(
        self,
        target_type: str,
        target_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[StockLog]:
        """
        특정 대상(예: target_type="MATERIAL" 또는 "PRODUCT")과 target_id에 해당하는
        재고 변동 이력 목록을 페이징하여 조회합니다.
        """
        pass

    @abstractmethod
    async def list_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[StockLog]:
        """
        특정 기간(시작일~종료일) 동안 발생한 재고 변동 이력 목록을 조회합니다.
        """
        pass