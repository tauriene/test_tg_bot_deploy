from aiogram import Router, F
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from bot.keyboards import get_models_kb, cancel_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import asyncio
from bot.db import add_user, get_requests_text_count, add_request, MAX_TEXT_PER_DAY

router = Router()

class Chat(StatesGroup):
    text = State()
    wait = State()


@router.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer("Привет")
    await add_user(tg_id=msg.from_user.id)


@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("Мои команды")


@router.message(Command("account"))
async def cmd_account(msg: Message):
    user = msg.from_user
    await msg.answer(
        "Подписка: стандартная\nМодель: GPT-4o mini /model\n\n📊 Статистика использования\nЗапросов в день: 0/5\n\nДата регистрации: "
    )


@router.message(F.text == "Отмена")
async def cancel(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(
        "Вы вышли из режима чата и вернулись в обычный режим!",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Command("chat"))
async def cmd_chat(msg: Message, state: FSMContext):
    await msg.answer("Введите ваш запрос:", reply_markup=cancel_kb)
    await state.set_state(Chat.text)


@router.message(Chat.text)
async def chat_response(msg: Message, state: FSMContext):
    user_req_count = await get_requests_text_count(tg_id=msg.from_user.id)

    if user_req_count < MAX_TEXT_PER_DAY:
        await msg.answer(f"Ищем ответ на: {msg.text}")

        await state.set_state(Chat.wait)
        await asyncio.sleep(5)

        await add_request(tg_id=msg.from_user.id, type="text")
        await msg.answer(
            f"Ваш ответ на: {msg.text}. Осталось запросов: {abs(user_req_count-MAX_TEXT_PER_DAY)}/5."
        )

        await state.set_state(Chat.text)
    else:
        await msg.answer(f"У вас осталось 0/5 запросов на сегодня. Попробуйте завтра.")


@router.message(Chat.wait)
async def chat_wait(msg: Message):
    await msg.answer("Подождите 5 секунд. Бот формирует ответ...")


@router.message(Command("model"))
async def cmd_model(msg: Message):
    await msg.answer("Выбрать модель ИИ", reply_markup=get_models_kb())


@router.callback_query(F.data.startswith("model_"))
async def cb_model(cb: CallbackQuery):
    model = cb.data.split("_")[1]
    await cb.answer("")
    await cb.message.edit_text(f"Отлично! Вы выбрали модель: {model}")
