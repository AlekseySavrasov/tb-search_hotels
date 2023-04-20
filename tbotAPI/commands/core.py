from telebot import types
from database.db_telebot import db
from tbotAPI.user_req_state import RequestState
from tbotAPI.keyboards import help_keyboard, button_help
from tbotAPI.create_bot import bot
from tbotAPI.commands.utils import bot_handlers
from typing import Dict


@bot.message_handler(commands=["start"])
def start_message(message: types.Message) -> None:
    """Функция, которая выводит стартовое информационное сообщение при введении команды /start"""
    bot.send_message(
        message.chat.id, f"Привет, {message.from_user.full_name}! Я - бот '{bot.get_me().first_name}', "
                         f"который помогает с поиском отелей через сайт https://www.hotels.com/.\n"
                         f"Для просмотра существующих команд введите команду /help .",
        reply_markup=button_help)


@bot.message_handler(commands=["help"])
def help_command(message: types.Message) -> None:
    """Функция выводящая список команд и их описание при вводе команды /help"""
    bot.send_message(
        message.chat.id, f"Список существующих команд:\n\n/lowprice — вывод самых дешёвых отелей в городе"
                         f"\n\n/highprice — вывод самых дорогих отелей в городе\n\n"
                         f"/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра"
                         f"\n\n/history — вывод истории поиска отелей",
        reply_markup=help_keyboard)


@bot.message_handler(commands=["lowprice"])
def search_lowprice(message: types.Message) -> None:
    """Функция начинает сбор данных для самых дешевых отелей в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/lowprice"
        data_request["sorting"]: str = "PRICE_LOW_TO_HIGH"


@bot.message_handler(commands=["highprice"])
def search_highprice(message: types.Message) -> None:
    """Функция начинает сбор данных для самых дорогих отелей в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/highprice"
        data_request["sorting"]: str = "PRICE_HIGH_TO_LOW"


@bot.message_handler(commands=["bestdeal"])
def search_bestdeal(message: types.Message) -> None:
    """Функция начинает сбор данных для отелей во введенном диапазоне цен и введенном диапазоне расстояния от центра
     в искомом городе"""
    bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
    bot.send_message(message.chat.id, "В каком городе хотите производить поиск отелей?")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        data_request["command"]: str = "/bestdeal"
        data_request["sorting"]: str = "DISTANCE"


@bot.message_handler(commands=["history"])
def history_command(message: types.Message, page=1, pages_count=10, previous_message=None) -> None:
    """Функция вывода последних десяти записей из таблицы истории запросов пользователя"""

    request_query = db.get_information()
    command, datetime_1, city_name, list_hotels = request_query[page - 1]
    buttons = types.InlineKeyboardMarkup()

    left = page - 1 if page != 1 else pages_count
    right = page + 1 if page != pages_count else 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(page)}/{str(pages_count)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buttons.add(left_button, page_button, right_button)

    text: str = f"Команда: *{command}*\nДата и время ввода команды: {datetime_1}\n" \
                f"Город поиска: {city_name}\nСписок найденных отелей: {list_hotels}"

    bot.send_message(message.chat.id, text, reply_markup=buttons)

    try:
        bot.delete_message(message.chat.id, previous_message.id)
    except BaseException:
        pass


@bot.callback_query_handler(func=lambda data: True)
def callback(data) -> None:
    """Обработчик callback"""
    if 'to' in data.data:
        page: int = int(data.data.split(' ')[1])
        history_command(data.message, page=page, previous_message=data.message)


@bot.message_handler(content_types=["text"])
def get_text_messages(message: types.Message) -> None:
    """Функция проверки введенного сообщения пользователя.
    Если вводится что-то кроме существующих команд,
    то выводится предложение ввести команду /help для информации о возможных действиях"""
    bot.send_message(
        message.chat.id,
        "Я не понимаю! Введите команду /help для вывода списка существующих команд.",
        reply_markup=button_help
    )


bot_handlers.register_handler()
