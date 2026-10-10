from typing import List, Optional
from app.domain.models.material import Material
from app.domain.schemas.material import MaterialCreate, MaterialUpdate
from app.domain.exceptions import (
    MaterialNotFoundException,
    DuplicateSKUException,
    InsufficientStockException,
)
from app.domain.repository_interfaces.material_repository import (
    MaterialRepositoryInterface,
)


class MaterialService:
    """
    원자재(Material) 관련 비즈니스 유스케이스를 처리하는 어플리케이션 서비스
    """

    def __init__(self, material_repo: MaterialRepositoryInterface):
        # 의존성 주입(Dependency Injection):
        # 구체적인 DB 리포지토리가 아닌 인터페이스에 의존합니다.
        self.material_repo = material_repo

    async def create_material(self, schema: MaterialCreate) -> Material:
        """
        새로운 원자재를 등록합니다.
        - 중복 코드(SKU)가 존재할 경우 DuplicateSKUException 예외를 발생시킵니다.
        """
        existing_material = await self.material_repo.get_by_code(schema.code)
        if existing_material:
            raise DuplicateSKUException(sku=schema.code)

        new_material = Material(
            code=schema.code,
            name=schema.name,
            category=schema.category,
            current_stock=schema.current_stock,
            safety_stock=schema.safety_stock,
            unit=schema.unit,
        )
        return await self.material_repo.save(new_material)

    async def get_material_by_id(self, material_id: int) -> Material:
        """
        ID로 단일 원자재를 조회합니다.
        - 존재하지 않을 경우 MaterialNotFoundException 예외를 발생시킵니다.
        """
        material = await self.material_repo.get_by_id(material_id)
        if not material:
            raise MaterialNotFoundException(material_id=material_id)
        return material

    async def get_all_materials(self, skip: int = 0, limit: int = 100) -> List[Material]:
        """
        전체 원자재 목록을 페이징하여 조회합니다.
        """
        return await self.material_repo.get_all(skip=skip, limit=limit)

    # ---- API 엔드포인트(materials.py)가 부르는 이름들 ----

    async def list_materials(self, skip: int = 0, limit: int = 100) -> List[Material]:
        return await self.get_all_materials(skip=skip, limit=limit)

    async def get_material(self, material_id: int) -> Optional[Material]:
        """없으면 None을 반환합니다. (API가 404로 변환)"""
        return await self.material_repo.get_by_id(material_id)

    async def adjust_stock(
        self, material_id: int, quantity_change: float, reason: str
    ) -> Material:
        """
        재고를 증감합니다. (양수: 입고, 음수: 출고)
        - 결과 재고가 음수가 되면 InsufficientStockException 발생
        - reason은 아직 저장하지 않습니다. (재고 이력 기능은 추후 연결)
        """
        material = await self.get_material_by_id(material_id)
        new_stock = material.current_stock + quantity_change
        if new_stock < 0:
            raise InsufficientStockException(
                target_name=material.name,
                current_stock=material.current_stock,
                required_stock=abs(quantity_change),
            )
        material.current_stock = new_stock
        return await self.material_repo.save(material)

    # ------------------------------------------------------

    async def add_stock(self, material_id: int, amount: float) -> Material:
        """
        원자재 입고 처리 (재고 수량 증가) 유스케이스
        - 수량이 0 이하일 경우 ValueError 발생
        """
        if amount <= 0:
            raise ValueError("입고 수량은 0보다 커야 합니다.")

        material = await self.get_material_by_id(material_id)
        material.current_stock += amount

        return await self.material_repo.save(material)

    async def delete_material(self, material_id: int) -> bool:
        """
        원자재를 삭제합니다.
        """
        # 먼저 원자재가 존재하는지 확인
        await self.get_material_by_id(material_id)
        return await self.material_repo.delete(material_id)