from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(
  settings.database_url,
  echo=False,
  pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
  engine,
  class_=AsyncSession,
  expire_on_commit=False,
  autocommit=False,
  autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
  async with async_session_maker() as session:
    try:
      yield session
      await session.commit()
    except SQLAlchemyError:
      await session.rollback()
      raise
    finally:
      await session.close()


async def check_db_connection() -> bool:
  try:
    async with async_session_maker() as session:
      await session.execute(text("SELECT 1"))
    return True
  except SQLAlchemyError:
    return False
