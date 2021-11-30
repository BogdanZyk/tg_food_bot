from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from database import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
  photo = State()
  name = State()
  description = State()
  price = State()

async def make_changes_command(message: types.Message):
  global ID
  ID = message.from_user.id
  await bot.send_message(message.from_user.id, 'Setting Admin', reply_markup = admin_kb.button_case_admin)
  await message.delete()

# начало диалога загрузки нового пункта меню
async def cm_start(message : types.Message):
  if message.from_user.id == ID:
    await FSMAdmin.photo.set()
    await message.reply('1 - Загрузите фото')

#Выход из состояний
async def cancel_handler(message : types.Message,state: FSMContext):
  if message.from_user.id == ID:
      current_state = await state.get_state()
      if current_state is None:
        return
      await state.finish()
      await message.reply('ОК')

#1 ответ id фото в словарь
async def load_photo(message: types.Message, state: FSMContext):
  if message.from_user.id == ID:
      async with state.proxy() as data:
          data['photo'] = message.photo[0].file_id
      await FSMAdmin.next()
      await message.reply('2 - Введите название ')

#2 ответ название
async def load_name(message : types.Message, state: FSMContext):
  if message.from_user.id == ID:
      async with state.proxy() as data:
            data['name'] = message.text
      await FSMAdmin.next()
      await message.reply('3 - Введите описание')

#3 ответ описание
async def load_description(message : types.Message, state: FSMContext):
  if message.from_user.id == ID:
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.reply('4 - Укажите цену')

#4 ответ цена и используем данные
async def load_price(message : types.Message, state: FSMContext):
  if message.from_user.id == ID:
    async with state.proxy() as data:
        data['price'] = message.text
    await message.reply('Блюдо успешно добавлено!')
    await sqlite_db.sql_add_command(state)
    await state.finish()
    
async def del_callback_run(callback_query: types.CallbackQuery):
  await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
  await callback_query.answer(text= f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)

async def delete_item(message : types.Message):
  if message.from_user.id == ID:
    read = await sqlite_db.sql_read2()
    for ret in read:
      await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}',\
         reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))
 
def register_handlers_admin(dp : Dispatcher):
  dp.register_message_handler(make_changes_command, commands = ["moderator"], is_chat_admin = True)
  dp.register_message_handler(cm_start, commands = ['Загрузить'], state = None)
  dp.register_message_handler(cancel_handler, state="*", commands = 'отмена')
  dp.register_message_handler(cancel_handler, Text( equals = 'отмена', ignore_case = True),state = "*")
  dp.register_message_handler(load_photo, content_types =['photo'], state = FSMAdmin.photo )
  dp.register_message_handler(load_name, state = FSMAdmin.name)
  dp.register_message_handler(load_description, state = FSMAdmin.description)
  dp.register_message_handler(load_price, state = FSMAdmin.price)
  dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
  dp.register_message_handler(delete_item, commands=['Удалить'])
