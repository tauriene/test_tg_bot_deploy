import asyncio
import logging
from aiogram import Bot, Dispatcher

from bot.utils.ui_commands import set_ui_commands
from bot.utils.config import settings
from bot.handlers import main_router
from bot.db import init_db

logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - [%(levelname)s] - %(name)s - "
    "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)

logger = logging.getLogger(__name__)


async def on_startup():
    await init_db()


async def main():
    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_router(main_router)

    await set_ui_commands(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
