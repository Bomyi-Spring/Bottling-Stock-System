from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title="Bottling Inventory System API",
    description="보틀링 재고 관리 및 원자재 차감, 생산 감사 이력 추적 시스템",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 미들웨어 설정 (프론트엔드 연동 지원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 허용할 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API v1 라우터 등록 (/api/v1 prefix 적용)
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
async def health_check():
    """
    서버 상태 체크용 헬스 케어 엔드포인트
    """
    return {
        "status": "ok",
        "app_name": "Bottling Inventory System",
        "version": "1.0.0",
    }