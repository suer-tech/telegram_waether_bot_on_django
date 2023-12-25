from telebot import types

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item = types.KeyboardButton("Узнать погоду")
markup.add(item)