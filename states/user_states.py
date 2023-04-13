from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    start = State()
    status = State()
    add_data = State()
    add_region = State()
    add_rooms = State()
    add_photos = State()
    add_home_data = State()
    add_price = State()
    add_phone_number = State()
    select_region = State()
    select_rooms = State()
    delete_data = State()
    get_status = State()
