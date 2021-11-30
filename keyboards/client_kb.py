from aiogram.types import ReplyKeyboardMarkup, KeyboardButton #,ReplyKeyboardRemove

b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Расположение')
btn_menu = KeyboardButton('Меню')
btn_pizz = KeyboardButton('Пицца')
btn_burger= KeyboardButton('Бургеры')
btn_return = KeyboardButton('Назад')
btn_size1 = KeyboardButton('Пицца 30см')
btn_size2 = KeyboardButton('Пицца 40см')
# b4 = KeyboardButton('поделиться номером',request_contact=True)
# b5 = KeyboardButton('отправить где я', request_location=True)

kb_menu = ReplyKeyboardMarkup(resize_keyboard = True)
kb_menu.add(btn_menu)

kb_subcategory = ReplyKeyboardMarkup(resize_keyboard = True)
kb_subcategory.add(btn_burger, btn_pizz, btn_return)

kb_piz_category = ReplyKeyboardMarkup(resize_keyboard = True)
kb_piz_category.add(btn_size2, btn_size1, btn_return)

kb_client = ReplyKeyboardMarkup(resize_keyboard = True)
kb_client.add(btn_burger)