import sys
import asyncio

# Windows에서 psycopg 비동기 모드를 쓰기 위한 설정 (반드시 맨 위에)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.database import engine, Base

# 모델을 import해야 Base가 테이블 정보를 알 수 있습니다
import app.infrastructure.models.material_model
import app.infrastructure.models.product_model
import app.infrastructure.models.stock_log_model


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("테이블 생성 완료")


asyncio.run(main())