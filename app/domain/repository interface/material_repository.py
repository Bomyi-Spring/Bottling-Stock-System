from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.material import Material


class MaterialRepositoryInterface(ABC):
    """
    원자재(Material) 리포지토리 추상 인터페이스.
    인프라 계층의 실제 DB 구현체(SQLAlchemy 등)는 이 클래스를 상속받아 구현해야 합니다.
    """

    @abstractmethod
    def save(self, material: Material) -> Material:
        """
        새로운 원자재를 저장하거나 기존 원자재 정보를 업데이트합니다.
        """
        pass

    @abstractmethod
    def get_by_id(self, material_id: int) -> Optional[Material]:
        """
        ID로 단일 원자재를 조회합니다. 존재하지 않을 경우 None을 반환합니다.
        """
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Material]:
        """
        원자재 고유 코드(예: MAT-001)로 단일 원자재를 조회합니다.
        """
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Material]:
        """
        원자재 목록을 페이징하여 조회합니다.
        """
        pass

    @abstractmethod
    def delete(self, material_id: int) -> bool:
        """
        ID에 해당하는 원자재를 삭제합니다. 성공 시 True, 실패 시 False를 반환합니다.
        """
        pass