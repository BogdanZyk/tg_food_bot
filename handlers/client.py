from aiogram import types, Dispatcher
from aiogram.dispatcher.dispatcher import Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from database import sqlite_db


# клиент часть
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup = kb_client)
        # await message.delete()
    except:
      await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/PizzaTested_bot')

async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Пн-Вс с 9:00 до 23:00')

async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул. Колотушкина 34')

async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands = ['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands = ['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands = ['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])