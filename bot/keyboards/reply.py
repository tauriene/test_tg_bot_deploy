from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Аккаунт")],
        [KeyboardButton(text="Модель")],
        [KeyboardButton(text="Начать чат")],
    ],
    resize_keyboard=True,
)

cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена")]],
    resize_keyboard=True,
    input_field_placeholder="Введите запрос...",
)
