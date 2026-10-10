from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.material import Material
from app.domain.repository_interfaces.material_repository import MaterialRepositoryInterface
from app.infrastructure.models.material_model import MaterialORM


class SqlAlchemyMaterialRepository(MaterialRepositoryInterface):
    """
    SQLAlchemy 비동기 세션을 사용하는 원자재(Material) 구체 리포지토리
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, material_id: int) -> Optional[Material]:
        """
        ID로 단일 원자재를 조회합니다.
        DB에서 꺼낸 ORM 객체를 .to_domain()을 통해 순수 도메인 객체로 변환하여 반환합니다.
        """
        result = await self.session.get(MaterialORM, material_id)
        if not result:
            return None
        return result.to_domain()

    async def get_by_code(self, code: str) -> Optional[Material]:
        """
        원자재 고유 코드(SKU)로 단일 원자재를 조회합니다.
        """
        stmt = select(MaterialORM).where(MaterialORM.code == code)
        result = await self.session.execute(stmt)
        orm_material = result.scalars().first()
        if not orm_material:
            return None
        return orm_material.to_domain()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Material]:
        """
        전체 원자재 목록을 페이징(skip, limit) 처리하여 조회합니다.
        """
        stmt = select(MaterialORM).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        orm_list = result.scalars().all()
        return [orm.to_domain() for orm in orm_list]

    async def save(self, material: Material) -> Material:
        """
        원자재 도메인 객체를 DB에 저장(INSERT 또는 UPDATE)합니다.
        - id가 없거나 DB에 존재하지 않으면 새 레코드 추가
        - id가 존재하면 기존 레코드 업데이트
        """
        if material.id:
            # 기존 레코드 업데이트 조회
            existing_orm = await self.session.get(MaterialORM, material.id)
            if existing_orm:
                existing_orm.code = material.code
                existing_orm.name = material.name
                existing_orm.category = material.category
                existing_orm.current_stock = material.current_stock
                existing_orm.safety_stock = material.safety_stock
                existing_orm.unit = material.unit
                # flush를 통해 세션 내 반영 후 도메인 객체로 변환해 반환
                await self.session.commit()
                return existing_orm.to_domain()

        # 신규 등록
        new_orm = MaterialORM.from_domain(material)
        self.session.add(new_orm)
        await self.session.commit()  # DB에 전송하여 자동 생성된 ID값 확보
        await self.session.refresh(new_orm)
        return new_orm.to_domain()

    async def delete(self, material_id: int) -> bool:
        """
        ID로 원자재 레코드를 삭제합니다.
        """
        orm_material = await self.session.get(MaterialORM, material_id)
        if not orm_material:
            return False
        await self.session.delete(orm_material)
        await self.session.flush()
        return True