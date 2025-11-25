from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.config import Config


def new_session_maker(config: Config) -> async_sessionmaker[AsyncSession]:
    database_uri = f'postgresql+asyncpg://{config.postgres_user}:' \
                   f'{config.postgres_password}@{config.postgres_host}:' \
                   f'{config.postgres_port}/{config.postgres_db}'

    engine = create_async_engine(
        database_uri,
        pool_size=15,
        max_overflow=15,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )