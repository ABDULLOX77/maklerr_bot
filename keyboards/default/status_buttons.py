from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

status_buttons = ReplyKeyboardMarkup(
    keyboard=[
    [
        KeyboardButton(text="Sotiladi"),
        KeyboardButton(text="Ijaraga")
    ],
    [
        KeyboardButton(text="⬅️ Ortga")
    ]
    ],
    resize_keyboard=True
)