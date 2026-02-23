from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="запуск бота"),
        BotCommand(command="account", description="детали аккаунта"),
        BotCommand(command="chat", description="начать чат с ИИ"),
        BotCommand(command="model", description="выбрать модель для генерации"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
