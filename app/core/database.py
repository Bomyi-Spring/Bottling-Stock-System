from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# PostgreSQL 접속 정보 (환경에 맞게 호스트, 계정 정보가 설정됩니다)
DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/bottling_db"

# 1. Async Engine 생성
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# 2. AsyncSessionLocal 생성
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 3. Base 클래스 생성
Base = declarative_base()


# 4. DB 세션 의존성 주입 함수
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session