from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.db.models import Base

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite")

async_session = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
