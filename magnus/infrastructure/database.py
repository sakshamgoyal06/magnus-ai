from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from magnus.infrastructure.config import Settings, get_settings


class Base(DeclarativeBase):
    pass


def _async_connect_args(database_url: str) -> dict:
    lowered = database_url.lower()
    if "supabase.co" in lowered or "ssl=require" in lowered:
        return {"ssl": True}
    return {}


def create_engine(settings: Settings | None = None) -> AsyncEngine:
    cfg = settings or get_settings()
    return create_async_engine(
        cfg.database_url,
        pool_pre_ping=True,
        connect_args=_async_connect_args(cfg.database_url),
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def check_database_connection(engine: AsyncEngine) -> bool:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return True


async def get_db_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
