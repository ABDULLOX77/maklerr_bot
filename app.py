from aiogram import executor

from loader import dp, homes_db, region_db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    try:
        region_db.create_table_region()
        region_db.add_data(status="status", region="region", farqiyo="farqiyo")
    except Exception as err:
        print(err)

    try:
        homes_db.create_table_homes()
    except Exception as err:
        print(err)
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
