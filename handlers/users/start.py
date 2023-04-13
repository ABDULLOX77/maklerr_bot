from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main_buttons import main_buttons
from states.user_states import UserState
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main_buttons)


@dp.message_handler(CommandStart(), state=UserState)
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=main_buttons)
    await state.finish()

