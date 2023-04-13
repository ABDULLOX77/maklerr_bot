from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

regions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Bektemir", callback_data="Bektemir"),
            InlineKeyboardButton(text="Mirobod", callback_data="Mirobod"),
        ],
        [
            InlineKeyboardButton(text="Mirzo Ulug'bek", callback_data="Mirzo Ulug'bek"),
            InlineKeyboardButton(text="Olmazor", callback_data="Olmazor"),
        ],
        [
            InlineKeyboardButton(text="Sergeli", callback_data="Sergeli"),
            InlineKeyboardButton(text="Yangi hayot", callback_data="Yangi hayot"),
        ],
        [
            InlineKeyboardButton(text="Uchtepa", callback_data="Uchtepa"),
            InlineKeyboardButton(text="Shayxontohur", callback_data="Shayxontohur"),
        ],
        [
            InlineKeyboardButton(text="Yashnobod", callback_data="Yashnobod"),
            InlineKeyboardButton(text="Chilonzor", callback_data="Chilonzor"),
        ],
        [
            InlineKeyboardButton(text="Yunusobod", callback_data="Yunusobod"),
            InlineKeyboardButton(text="Yakkasaroy", callback_data="Yakkasaroy"),
        ],
    ]
)
