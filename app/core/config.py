import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Bottling Management System"
    API_V1_STR: str = "/api/v1"
    
    # PostgreSQL 데이터베이스 연결 URL (환경에 맞게 계정/비밀번호/DB명을 조정 가능)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://postgres:postgres@localhost:5432/bottling_db"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


# 외부 서비스 및 엔드포인트에서 참조할 settings 객체
settings = Settings()