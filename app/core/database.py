from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. DB 접속 URL 설정 (PostgreSQL 예시)
# 실제 운영 환경에서는 .env 환경변수에서 불러와 사용합니다.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/bottling_db"

# 2. Engine 생성 (DB와의 물리적 연결 통로)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 끊어진 커넥션을 자동으로 감지하여 재연결
    pool_size=10,        # 동시 유지할 기본 커넥션 수
    max_overflow=20      # 요청 폭증 시 추가 허용 커넥션 수
)

# 3. SessionLocal 생성 (1회용 DB 작업 창구를 찍어내는 공장)
SessionLocal = sessionmaker(
    autocommit=False,  # 개발자가 명시적으로 commit()을 호출해야 저장
    autoflush=False,   # 쿼리 실행 전 자동 flush 방지
    bind=engine
)

# 4. Base 클래스 생성 (모든 도메인 ORM 모델의 부모 클래스)
Base = declarative_base()

# 5. DB 세션 의존성 주입 함수 (FastAPI 전용)
def get_db() -> Generator:
    """
    API 요청이 들어올 때 DB 세션을 생성하고,
    처리가 끝나면(finally) 반드시 세션을 닫아 자원 누수를 방지합니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()