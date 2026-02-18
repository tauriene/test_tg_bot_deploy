import asyncio
from aiogram import Bot, Dispatcher
from bot.config_reader import config
from bot.handlers import main_router
from bot.db import init_db


async def on_startup():
    print("Bot started")
    await init_db()


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.include_router(main_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
