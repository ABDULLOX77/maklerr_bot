from aiogram.types import Message
from loader import dp
from data.config import ADMINS
from keyboards.default.status_buttons import status_buttons
from states.user_states import UserState


@dp.message_handler(text="Ma'lumot olish", user_id=ADMINS)
async def add_data(message: Message):
    await message.answer("sdasadas", reply_markup=status_buttons)
    await UserState.status.set()
