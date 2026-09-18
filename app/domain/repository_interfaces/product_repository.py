from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.product import Product


class ProductRepositoryInterface(ABC):
    """
    Product 도메인 엔티티를 관리하기 위한 추상 리포지토리 인터페이스
    """

    @abstractmethod
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """
        ID로 단일 상품을 조회합니다.
        """
        pass

    @abstractmethod
    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """
        SKU 고유 코드로 단일 상품을 조회합니다.
        """
        pass

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        전체 상품 목록을 페이징하여 조회합니다.
        """
        pass

    @abstractmethod
    async def save(self, product: Product) -> Product:
        """
        새로운 상품을 생성하거나 기존 상품 정보를 업데이트합니다.
        """
        pass

    @abstractmethod
    async def update_stock(self, product_id: UUID, quantity_change: int) -> Optional[Product]:
        """
        상품의 재고 수량을 변경합니다. (양수: 입고, 음수: 출고)
        """
        pass

    @abstractmethod
    async def delete(self, product_id: UUID) -> bool:
        """
        ID로 상품을 삭제합니다. 성공 시 True를 반환합니다.
        """
        pass