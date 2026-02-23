from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Аккаунт", style="primary")],
        [KeyboardButton(text="Модель", style="primary")],
        [KeyboardButton(text="Начать чат", style="primary")],
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена", style="danger")]],
    resize_keyboard=True,
    input_field_placeholder="Введите запрос...",
)
