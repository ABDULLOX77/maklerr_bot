from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ma'lumot olish"),
            KeyboardButton(text="Ma'lumot qo'shish")
        ],
        [
            KeyboardButton(text="O'chirish"),
        ]
    ],
    resize_keyboard=True
)

back_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bekor qilish ❌")
        ]
    ],
    resize_keyboard=True
)
