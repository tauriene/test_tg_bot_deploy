from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums.parse_mode import ParseMode

from bot.keyboards import main_kb, cancel_kb
from bot.utils.generators import genetate_text
from bot.db import (
    add_user,
    get_requests_count,
    add_request,
    MAX_REQUESTS_PER_DAY,
)

router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message):
    await add_user(tg_id=msg.from_user.id)
    await msg.answer(
        "Привет! 🤖\nЯ бот с ИИ — могу помочь с учёбой, кодом, текстами, идеями и любыми вопросами.\n\n Введи команду /chat или нажми кнопку, и мы начнем!",
        reply_markup=main_kb,
    )


@router.message(F.text == "Аккаунт")
@router.message(Command("account"))
async def cmd_account(msg: Message):
    user_req_count = await get_requests_count(
        tg_id=msg.from_user.id,
    )
    await msg.answer(
        f"Подписка: стандартная\nМодель: GPT-4o mini /model\n\n📊 Статистика использования\n"
        f"Осталось запросов на сегодня: {MAX_REQUESTS_PER_DAY - user_req_count}/5\n"
    )


@router.message(F.text == "Модель")
@router.message(Command("model"))
async def cmd_model(msg: Message):
    await msg.answer(
        "У вас выбрана модель GPT-4o mini.\n\nДобавление других моделей в разработке..."
    )


class Chat(StatesGroup):
    text = State()
    wait = State()


@router.message(F.text == "Начать чат")
@router.message(Command("chat"))
async def cmd_chat(msg: Message, state: FSMContext):
    await msg.answer("Введите ваш запрос:", reply_markup=cancel_kb)
    await state.set_state(Chat.text)


@router.message(F.text == "Отмена")
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Вы вышли из режима чата и вернулись в обычный режим!",
        reply_markup=main_kb,
    )


@router.message(Chat.text)
async def chat_response(msg: Message, state: FSMContext):
    user_req_count = await get_requests_count(tg_id=msg.from_user.id)

    if user_req_count < MAX_REQUESTS_PER_DAY:
        status_msg = await msg.answer("Ищу ответ...")
        await state.set_state(Chat.wait)

        response = await genetate_text(msg.text)
        if response["ok"]:
            await add_request(tg_id=msg.from_user.id)

            await msg.answer(response["text"], parse_mode=ParseMode.MARKDOWN)
            await msg.answer(
                f"Ваш ответ. Осталось текстовых запросов на сегодня: {MAX_REQUESTS_PER_DAY - user_req_count - 1}/5."
            )

            await state.set_state(Chat.text)
        else:
            await msg.answer("Произошла ошибка! Попробуйте позже.")
        await status_msg.delete()
    else:
        await msg.answer(
            f"У вас осталось 0/5 текстовых запросов на сегодня. Попробуйте завтра."
        )


@router.message(Chat.wait)
async def chat_wait(msg: Message):
    await msg.answer("Подождите 5 секунд. Бот формирует ответ...")
