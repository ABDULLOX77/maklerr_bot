from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentTypes, MediaGroup
from aiogram.dispatcher import FSMContext
from loader import dp, homes_db
from data.config import ADMINS
from states.user_states import UserState
from keyboards.default.status_buttons import status_buttons
from keyboards.default.finish_button import finish_buttons
from keyboards.inline.regions_keyboards import regions_keyboard
from keyboards.default.main_buttons import main_buttons
import asyncio


@dp.message_handler(text="Ma'lumot qo'shish", user_id=ADMINS)
async def add_data(message: Message):
    await message.answer("Turini tanlang", reply_markup=status_buttons)
    await UserState.add_data.set()


@dp.message_handler(text="⬅️ Ortga", user_id=ADMINS, state=UserState.add_data)
async def add_ortga(message: Message, state: FSMContext):
    await message.answer("Kerakli bolimni tanlang", reply_markup=main_buttons)
    await state.finish()


@dp.message_handler(text="Ijaraga", user_id=ADMINS, state=UserState.add_data)
async def add_data2(message: Message):
    status = message.text
    homes_db.add_data(f"{status}", "none", 0, "none", "none", 0, "none")
    await message.answer("Tumanni tanlang", reply_markup=regions_keyboard)
    rem = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await rem.delete()
    await UserState.add_region.set()


@dp.message_handler(text="Sotiladi", user_id=ADMINS, state=UserState.add_data)
async def add_data_2(message: Message):
    status = message.text
    homes_db.add_data(f"{status}", "none", 0, "none", "none", 0, "none")
    await message.answer("Tumanni tanlang", reply_markup=regions_keyboard)
    rem = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await rem.delete()
    await UserState.add_region.set()


@dp.message_handler(state=UserState.add_data, user_id=ADMINS)
async def bad_text(message: Message):
    rem = await message.answer("Iltimos bu yerda yozmang ✋\nTurni tanlang️ 👇")
    await asyncio.sleep(5)
    await rem.delete()
    await message.delete()


@dp.callback_query_handler(lambda c: True, state=UserState.add_region, user_id=ADMINS)
async def add_data3(call: CallbackQuery):
    get = homes_db.get_last_data()
    home_id = get[0]
    homes_db.update_region(home_id=home_id[0], region=call.data)
    await call.message.edit_text(f"{call.data} tumani tanlandi")
    await call.message.answer("Uyning honalari sonini kriting")
    await UserState.add_rooms.set()


@dp.message_handler(state=UserState.add_region, user_id=ADMINS)
async def bad_text(message: Message):
    rem = await message.answer("Iltimos bu yerda yozmang ✋\nTumanlardan birini tanlang 👆")
    await asyncio.sleep(5)
    await rem.delete()
    await message.delete()


@dp.message_handler(state=UserState.add_rooms, user_id=ADMINS)
async def add_data4(message: Message):
    get = homes_db.get_last_data()
    home_id = get[0]
    if message.text.isdigit():
        homes_db.update_rooms(home_id=home_id[0], rooms=message.text)
        await message.answer("Uy haqida ma'lumotlarni kriting")
        await UserState.add_home_data.set()
    else:
        rem = await message.answer("Xonalar sonini raqam bilan kiriting 🔢")
        await asyncio.sleep(5)
        await rem.delete()
        await message.delete()


@dp.message_handler(state=UserState.add_home_data, user_id=ADMINS)
async def add_data5(message: Message):
    get = homes_db.get_last_data()
    home_id = get[0]
    homes_db.update_home_data(home_id=home_id[0], home_data=message.text)
    await message.answer("Uyning narxini kriting")
    await UserState.add_price.set()


@dp.message_handler(state=UserState.add_price, user_id=ADMINS)
async def add_data5(message: Message):
    get = homes_db.get_last_data()
    home_id = get[0]
    if message.text.isdigit():
        homes_db.update_price(home_id=home_id[0], price=message.text)
        await message.answer("Uy egasi yoki maklerning telfon raqamini kriting")
        await UserState.add_phone_number.set()
    else:
        rem = await message.answer("Uyning narxini raqam bilan kiriting 🔢")
        await asyncio.sleep(5)
        await rem.delete()
        await message.delete()


@dp.message_handler(state=UserState.add_phone_number, user_id=ADMINS)
async def add_data5(message: Message):
    get = homes_db.get_last_data()
    home_id = get[0]
    homes_db.update_phone_number(home_id=home_id[0], phone_number=message.text)
    await message.answer("Iltimos uyning rasmlarini 1 tadan yuboring")
    await UserState.add_photos.set()


@dp.message_handler(state=UserState.add_photos, user_id=ADMINS, content_types=ContentTypes.PHOTO)
async def add_data6(message: Message):
    get = homes_db.get_last_data()
    home_id = get[0]
    photos = homes_db.select_id(home_id[0])
    if photos[0][4] == "none":
        homes_db.update_photos(home_id=home_id[0], photos=message.photo[-1].file_id)
    else:
        homes_db.update_photos(home_id=home_id[0], photos=f"{photos[0][4]}, {message.photo[-1].file_id}")
    await message.answer("Yana rasm yuborishinginz mumkun", reply_markup=finish_buttons)


@dp.message_handler(text="Ma'lumot qo'shishni yakunlash", state=UserState.add_photos, user_id=ADMINS)
async def finish_add_data(message: Message, state: FSMContext):
    get = homes_db.get_last_data()
    home_id = get[0][0]
    i = homes_db.select_id(home_id=home_id)
    i = i[0]
    album = MediaGroup()
    photos = i[4].split(",")
    num = len(photos)
    for j in photos:
        num -= 1
        album.attach_photo(photo=j.strip())
        if num == 1:
            break
    album.attach_photo(photo=photos[-1].strip(), caption=f"#{i[1]}\n\nid: {i[0]}\n\n{i[2]} tumani\n{i[3]} xona\n"
                                                         f"{i[5]}\n\nNarxi: ${i[6]}\n\nTelefon: {i[7]}")
    await message.answer_media_group(media=album)
    await message.answer("Ma'lumotlar bazaga qo'shildi", reply_markup=main_buttons)
    await state.finish()


@dp.message_handler(state=UserState.add_photos, user_id=ADMINS)
async def check_photo(message: Message):
    rem = await message.answer("Iltimos bu yerda yozmang ✋\nUyning rasmlarini 1 tadan yuboring ☝️")
    await asyncio.sleep(5)
    await rem.delete()
    await message.delete()
