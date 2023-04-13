import asyncio

from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, homes_db
from data.config import ADMINS
from keyboards.default.main_buttons import main_buttons, back_button
from states.user_states import UserState


@dp.message_handler(text="O'chirish", user_id=ADMINS)
async def delete_data(message: Message):
    await message.answer("O'chirmoqchi bolgan ma'lumotingizni idsini yuboring", reply_markup=back_button)
    await UserState.delete_data.set()


@dp.message_handler(text="Bekor qilish ❌", state=UserState.delete_data, user_id=ADMINS)
async def back_button_def(message: Message, state: FSMContext):
    await message.answer("O'chirish bekor qilindi", reply_markup=main_buttons)
    await state.finish()


@dp.message_handler(state=UserState.delete_data, user_id=ADMINS)
async def delete_data2(message: Message, state: FSMContext):
    if message.text.isdigit():
        data = homes_db.select_all_homes()
        check = False
        for i in data:
            if i[0] == int(message.text):
                check = True
                homes_db.delete_home(home_id=message.text)
        if check:
            await message.answer("Ma'lumot o'chirildi", reply_markup=main_buttons)
            await state.finish()
        else:
            await message.answer("Bunday idlik ma'lumot mavjud emas", reply_markup=main_buttons)
            await state.finish()
    else:
        rem = await message.answer("Iltimos idni raqamlar bilan kiriting 🔢")
        await asyncio.sleep(5)
        await rem.delete()
        await message.delete()