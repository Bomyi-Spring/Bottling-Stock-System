from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.material import Material


class MaterialRepositoryInterface(ABC):
    """
    원자재(Material) 리포지토리 추상 인터페이스 (비동기 통일 버전)
    """

    @abstractmethod
    async def save(self, material: Material) -> Material:
        pass

    @abstractmethod
    async def get_by_id(self, material_id: int) -> Optional[Material]:
        pass

    @abstractmethod
    async def get_by_code(self, code: str) -> Optional[Material]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Material]:
        pass

    @abstractmethod
    async def delete(self, material_id: int) -> bool:
        pass