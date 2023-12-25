import time
from environs import Env
from telebot import TeleBot, types
import logging
from .telegram_keyboard import markup
from .weather_api import get_weather_info_for_city

def start_telegram_bot():
    env = Env()
    env.read_env()

    TELEGRAM_TOKEN = env.str('TELEGRAM_TOKEN')
    bot = TeleBot(TELEGRAM_TOKEN)

    logging.basicConfig(filename='telegram_bot.log', level=logging.ERROR)

    user_states = {}  # Словарь для отслеживания состояний пользователей


    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        mess = f'Привет, {message.from_user.first_name}! Здесь можно узнать погоду для городов России.'
        bot.send_message(message.chat.id, mess, reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'Узнать погоду')
    def ask_for_city(message):
        user_states[message.chat.id] = "waiting_for_city"  # Устанавливаем состояние ожидания ввода города
        bot.send_message(message.chat.id, "Введите название города:")

    @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_city")
    def get_weather_for_city(message):
        try:
            city_name = message.text
            weather_message = get_weather_info_for_city(city_name)
            bot.send_message(message.chat.id, weather_message, reply_markup=markup)
            user_states[message.chat.id] = None  # Сбрасываем состояние ожидания
        except Exception as e:
            logging.error(f"Error in get_weather_for_city: {e}")
            bot.send_message(message.chat.id, 'Ошибка! Пожалуйста, нажмите Узнать погоду и введите корректное название города.', reply_markup=markup)

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, "Пожалуйста, используйте кнопки для взаимодействия.", reply_markup=markup)

    while True:
        bot.polling(none_stop=True)
        time.sleep(5)
