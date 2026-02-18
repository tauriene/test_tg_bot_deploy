from bot.db.models import User, async_session, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

MAX_TEXT_PER_DAY = 5


def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return inner


@connection
async def add_user(session: AsyncSession, tg_id: int):
    stmt = select(User).where(User.tg_id == tg_id)
    user = await session.scalar(stmt)

    if not user:
        session.add(User(tg_id=tg_id))
        await session.commit()


@connection
async def get_user(session: AsyncSession, tg_id: int):
    return await session.scalar(select(User).where(User.tg_id == tg_id))


@connection
async def add_request(session: AsyncSession, tg_id: int, type: str):
    req = Request(user_id=tg_id, type=type)
    session.add(req)
    await session.commit()


@connection
async def get_requests_text_count(session: AsyncSession, tg_id: int) -> int:
    stmt = select(func.count(Request.id)).where(
        Request.user_id == tg_id,
        Request.type == "text",
        func.date(Request.created_at) == datetime.utcnow().date(),
    )
    return await session.scalar(stmt) or 0
