from telebot.types import Message
from database.db_telebot import db
from tbotAPI.user_req_state import RequestState
from tbotAPI.keyboards import help_keyboard, button_help
from tbotAPI.create_bot import bot
from tbotAPI.commands.utils import bot_handlers
from typing import Dict


@bot.message_handler(commands=["start"])
def start_message(message: Message) -> None:
    """Функция, которая выводит стартовое информационное сообщение при введении команды /start"""
    bot.send_message(
        message.chat.id, f"Привет, {message.from_user.full_name}! Я - бот '{bot.get_me().first_name}', "
                         f"который помогает с поиском отелей через сайт https://www.hotels.com/.\n"
                         f"Для просмотра существующих команд введите команду /help .",
        reply_markup=button_help)


@bot.message_handler(commands=["help"])
def help_command(message: Message) -> None:
    """Функция выводящая список команд и их описание при вводе команды /help"""
    bot.send_message(
        message.chat.id, f"Список существующих команд:\n\n/lowprice — вывод самых дешёвых отелей в городе"
                         f"\n\n/highprice — вывод самых дорогих отелей в городе\n\n"
                         f"/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра"
                         f"\n\n/history — вывод истории поиска отелей",
        reply_markup=help_keyboard)


@bot.message_handler(commands=["lowprice"])
def search_lowprice(message: Message) -> None:
    """Функция начинает сбор данных для самых дешевых отелей в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/lowprice"
        data_request["sorting"]: str = "PRICE_LOW_TO_HIGH"


@bot.message_handler(commands=["highprice"])
def search_highprice(message: Message) -> None:
    """Функция начинает сбор данных для самых дорогих отелей в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/highprice"
        data_request["sorting"]: str = "PRICE_HIGH_TO_LOW"


@bot.message_handler(commands=["bestdeal"])
def search_bestdeal(message: Message) -> None:
    """Функция начинает сбор данных для отелей во введенном диапазоне цен и введенном диапазоне расстояния от центра
     в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/bestdeal"
        data_request["sorting"]: str = "DISTANCE"


@bot.message_handler(commands=["history"])
def history_command(message: Message) -> None:
    """Функция вывода последних десяти записей из таблицы истории запросов пользователя"""
    text: str = ""
    dict_db: Dict[int, str] = {
        0: "Команда: ",
        1: "Дата и время ввода команды: ",
        2: "Город поиска: ",
        3: "Список найденных отелей: "
    }

    if db.get_information():
        for i_string in db.get_information():
            for i_index, i_item in enumerate(i_string):
                text += f"{dict_db[i_index]}{i_item}\n"
            bot.send_message(message.from_user.id, text)
            text: str = ""
    else:
        bot.send_message(message.chat.id, "История запросов пуста")


@bot.message_handler(content_types=["text"])
def get_text_messages(message: Message) -> None:
    """Функция проверки введенного сообщения пользователя.
    Если вводится что-то кроме существующих команд,
    то выводится предложение ввести команду /help для информации о возможных действиях"""
    bot.send_message(
        message.chat.id,
        "Я не понимаю! Введите команду /help для вывода списка существующих команд.",
        reply_markup=button_help
    )


bot_handlers.register_handler()
