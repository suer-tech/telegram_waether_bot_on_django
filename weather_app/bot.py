from environs import Env
from telebot import TeleBot, types
from . weather_api import get_weather


def start_telegram_bot():
    env = Env()
    env.read_env()

    TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')
    bot = TeleBot(TELEGRAM_TOKEN)

    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("Погода")
        markup.add(item)

        bot.send_message(message.chat.id, "Hi there, I am EchoBot. Just say anything nice, and I'll say the exact same thing to you!",
                         reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'Погода')
    def ask_for_city(message):
        markup = types.ForceReply(selective=False)
        bot.send_message(message.chat.id, "Введите название города:", reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        weather_message = get_weather(message)
        bot.reply_to(message, weather_message.text)

    bot.polling(none_stop=True)