from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other
from database import sqlite_db


async def on_startup(_):
        print('Bot online now!')
        sqlite_db.sql_start()



admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)


executor.start_polling(dp, skip_updates = True, on_startup = on_startup)

