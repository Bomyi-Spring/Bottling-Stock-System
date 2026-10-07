from fastapi import APIRouter

from app.api.v1.endpoints import materials, products, stock_logs

api_router = APIRouter()

# 원자재 관리 엔드포인트 등록
api_router.include_router(
    materials.router,
    prefix="/materials",
    tags=["materials"],
)

# 완제품 및 보틀링 생산 엔드포인트 등록
api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"],
)

# 재고 변동 감사 이력 엔드포인트 등록
api_router.include_router(
    stock_logs.router,
    prefix="/stock-logs",
    tags=["stock-logs"],
)