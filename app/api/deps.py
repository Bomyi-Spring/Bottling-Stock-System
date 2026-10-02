from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.infrastructure.repositories.material_repository import SqlAlchemyMaterialRepository
from app.infrastructure.repositories.product_repository import SqlAlchemyProductRepository
from app.infrastructure.repositories.stock_log_repository import SqlAlchemyStockLogRepository
from app.services.material_service import MaterialService
from app.services.product_service import ProductService
from app.services.stock_log_service import StockLogService


# --- Repositories ---
def get_material_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyMaterialRepository:
    return SqlAlchemyMaterialRepository(session)


def get_product_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyProductRepository:
    return SqlAlchemyProductRepository(session)


def get_stock_log_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SqlAlchemyStockLogRepository:
    return SqlAlchemyStockLogRepository(session)


# --- Services ---
def get_material_service(
    material_repo: SqlAlchemyMaterialRepository = Depends(get_material_repository),
) -> MaterialService:
    return MaterialService(material_repo=material_repo)


def get_stock_log_service(
    stock_log_repo: SqlAlchemyStockLogRepository = Depends(get_stock_log_repository),
) -> StockLogService:
    return StockLogService(stock_log_repo=stock_log_repo)


def get_product_service(
    product_repo: SqlAlchemyProductRepository = Depends(get_product_repository),
    material_repo: SqlAlchemyMaterialRepository = Depends(get_material_repository),
    stock_log_service: StockLogService = Depends(get_stock_log_service),
) -> ProductService:
    return ProductService(
        product_repo=product_repo,
        material_repo=material_repo,
        stock_log_service=stock_log_service,
    )