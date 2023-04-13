import asyncio

from aiogram.types import Message, CallbackQuery, MediaGroup, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards.default.main_buttons import main_buttons, back_button
from keyboards.default.status_buttons import status_buttons
from loader import dp, homes_db, region_db, bot
from data.config import ADMINS
from keyboards.inline.regions_keyboards import regions_keyboard
from states.user_states import UserState


@dp.message_handler(text="Ma'lumot olish", user_id=ADMINS)
async def select_data(message: Message):
    await message.answer("Turini tanlang", reply_markup=status_buttons)
    await UserState.get_status.set()


@dp.message_handler(text="⬅️ Ortga", user_id=ADMINS, state=UserState.get_status)
async def select_back(message: Message, state: FSMContext):
    await message.answer("Kerakli bolimni tanlang", reply_markup=main_buttons)
    await state.finish()


@dp.message_handler(state=UserState.get_status, user_id=ADMINS)
async def get_status(message: Message):
    region_db.update_status(farqiyo="farqiyo", status=message.text)
    if message.text == "Sotiladi" or message.text == "Ijaraga":
        await message.answer("Toshkent shaxrining barcha tumanlari", reply_markup=back_button)
        await message.answer("Kerakli tumanni tanlang", reply_markup=regions_keyboard)
        await UserState.select_region.set()
    else:
        rem = await message.answer("Iltimos bu yerda yozmang ✋\nTurni tanlang️ 👇")
        await asyncio.sleep(5)
        await rem.delete()
        await message.delete()


@dp.message_handler(text="Bekor qilish ❌", state=UserState.select_region, user_id=ADMINS)
async def back_button_def(message: Message, state: FSMContext):
    await message.answer("Ma'lumot olish bekor qilindi bekor qilindi", reply_markup=main_buttons)
    await state.finish()


@dp.callback_query_handler(lambda c: True, state=UserState.select_region, user_id=ADMINS)
async def select_region(call: CallbackQuery):
    region_db.update_region(farqiyo="farqiyo", region=call.data)
    await call.message.edit_text("Necha xonali uy qidiryabsiz")
    await UserState.select_rooms.set()


@dp.message_handler(state=UserState.select_region, user_id=ADMINS)
async def bad_text(message: Message):
    rem = await message.answer("Iltimos bu yerda yozmang ✋\nTumanlardan birini tanlang 👆")
    await asyncio.sleep(5)
    await rem.delete()
    await message.delete()


@dp.message_handler(text="Bekor qilish ❌", state=UserState.select_rooms, user_id=ADMINS)
async def back_button_def(message: Message, state: FSMContext):
    await message.answer("Ma'lumot olish bekor qilindi bekor qilindi", reply_markup=main_buttons)
    await state.finish()


@dp.message_handler(state=UserState.select_rooms, user_id=ADMINS)
async def select_room(message: Message, state: FSMContext):
    if message.text.isdigit():
        region = region_db.select_region(farqiyo="farqiyo")
        data = homes_db.select_region(region=region[0][1])
        check = False
        for i in data:
            bad = region[0][0]
            album = MediaGroup()
            try:
                if i[3] == int(message.text) and i[1] == bad:
                    check = True
                    photos = i[4].split(",")
                    num = len(photos)
                    for j in photos:
                        num -= 1
                        album.attach_photo(photo=j.strip())
                        if num == 1:
                            break
                    album.attach_photo(photo=photos[-1].strip(),
                                       caption=f"#{i[1]}\n\nid: {i[0]}\n\n{i[2]} tumani\n{i[3]} xona\n"
                                               f"{i[5]}\n\nNarxi: ${i[6]}\n\nTelefon: {i[7]}")
                    await message.answer_media_group(media=album)
            except Exception as err:
                print(err)
        print(data)
        if check:
            await message.answer(f"{region[0][1]} tumanida shu ma'lumotlar topildi 👍", reply_markup=main_buttons)
            await state.finish()
        else:
            await message.answer(f"{region[0][1]} tumanida xech qanday ma'lumot topilmadi 😫", reply_markup=main_buttons)
            await state.finish()
    else:
        rem = await message.answer("Xonalar sonini raqam bilan kiriting 🔢")
        await asyncio.sleep(5)
        await rem.delete()
        await message.delete()
