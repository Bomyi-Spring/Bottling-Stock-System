from typing import List, Optional
from uuid import UUID

from app.domain.models.product import Product
from app.domain.schemas.product import ProductCreate, ProductUpdate
from app.domain.exceptions import (
    ProductNotFoundException,
    DuplicateSKUException,
    InsufficientStockException,
    MaterialNotFoundException,
)
from app.domain.repository_interfaces.product_repository import ProductRepositoryInterface
from app.domain.repository_interfaces.material_repository import MaterialRepositoryInterface


class ProductService:
    """
    완제품(Product) 생성, 조회 및 생산(원자재 자동 차감) 비즈니스 유스케이스 서비스
    """

    def __init__(
        self,
        product_repo: ProductRepositoryInterface,
        material_repo: MaterialRepositoryInterface,
    ):
        # 완제품 리포지토리와 원자재 리포지토리를 모두 주입받아 조율(Orchestration)합니다.
        self.product_repo = product_repo
        self.material_repo = material_repo

    async def create_product(self, schema: ProductCreate) -> Product:
        """
        새로운 완제품을 등록합니다.
        - SKU 중복 검사 수행
        """
        existing_product = await self.product_repo.get_by_sku(schema.sku)
        if existing_product:
            raise DuplicateSKUException(sku=schema.sku)

        new_product = Product(
            sku=schema.sku,
            name=schema.name,
            category=schema.category,
            current_stock=schema.current_stock,
            price=schema.price,
            recipe=schema.recipe,  # 레시피 예시: {"material_id_1": 1.0, "material_id_2": 2.0}
        )
        return await self.product_repo.save(new_product)

    async def get_product_by_id(self, product_id: UUID) -> Product:
        """
        ID로 단일 완제품을 조회합니다.
        - 존재하지 않을 경우 ProductNotFoundException 발생
        """
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(product_id=product_id)
        return product

    async def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        전체 완제품 목록을 페이징하여 조회합니다.
        """
        return await self.product_repo.list_all(skip=skip, limit=limit)

    async def produce_product(self, product_id: UUID, quantity: int) -> Product:
        """
        [핵심 비즈니스 유스케이스] 완제품 생산 및 원자재 자동 차감
        1. 생산 수량 검증 (quantity > 0)
        2. 완제품 존재 여부 및 레시피 확인
        3. 레시피에 필요한 모든 원자재의 재고가 충분한지 사전 검증 (부족 시 InsufficientStockException)
        4. 원자재 재고 차감 반영
        5. 완제품 재고 수량 증가 및 저장
        """
        if quantity <= 0:
            raise ValueError("생산 수량은 1개 이상이어야 합니다.")

        # 1. 완제품 조회
        product = await self.get_product_by_id(product_id)

        # 2. 레시피(BOM) 검증 및 필요한 원자재 재고 사전 확인
        # recipe 구조 예시: { material_id(int): required_amount_per_unit(float) }
        materials_to_update = []

        for mat_id, required_per_unit in product.recipe.items():
            required_total = required_per_unit * quantity
            material = await self.material_repo.get_by_id(mat_id)

            if not material:
                raise MaterialNotFoundException(material_id=mat_id)

            # 원자재 재고 부족 검증 (서비스 계층의 에러 수호자 역할!)
            if material.current_stock < required_total:
                raise InsufficientStockException(
                    item_name=material.name,
                    required=required_total,
                    current=material.current_stock,
                )

            # 차감할 원자재 객체와 차감 후 수량을 임시 저장
            materials_to_update.append((material, required_total))

        # 3. 모든 원자재의 재고가 충분함이 확인되었으므로 actual 재고 차감 진행
        for material, required_total in materials_to_update:
            material.current_stock -= required_total
            await self.material_repo.save(material)

        # 4. 완제품 재고 수량 증가
        product.current_stock += quantity
        updated_product = await self.product_repo.save(product)

        return updated_product