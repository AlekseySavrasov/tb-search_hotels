from telebot.types import Message, ReplyKeyboardMarkup
from rapidAPI.utils.rapidapi_requests import get_data_city, get_data_hotels
from tbotAPI.user_req_state import RequestState
from tbotAPI import keyboards
from tbotAPI.create_bot import bot
from database.db_telebot import db
from datetime import datetime
from re import fullmatch
from typing import Dict, List


def check_final_apply_user(message: Message) -> None:
    """
    Функция проверки подтверждения конечного запроса поиска отелей.
    Информация берется из внутреннего словаря бота.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        bot.send_message(
            message.chat.id,
            f"Это то, что вы ищите?(Да/Нет)\n\nГород: {data_request['name_city']}\nДата заезда: "
            f"{'-'.join(data_request['date_incoming'])}\nДата выезда: {'-'.join(data_request['date_outcoming'])}\n"
            f"Количество отелей: {data_request['amount_hotels']}\nФотографии: {data_request['download_photos']}\n"
            f"Количество фотографий: {data_request['amount_photos']}",
            reply_markup=keyboards.markup
        )


@bot.message_handler(state=RequestState.location_city)
def get_country(message: Message) -> None:
    """
    Функция проверки корректности введенного названия города.
    В зависимости от команды записывает название города, возможные места нахождения города, либо
    минимальную и максимальную цену за ночь во внутренний словарь бота,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text.isalpha():
        some_countries: Dict[str, str] = get_data_city(a_city=message.text)

        if len(some_countries) == 0:
            bot.send_message(message.chat.id, "Возможно, ошибка в названии города. Попробуйте еще раз!")
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
                data_request["name_city"]: str = message.text
                data_request["list_countries"]: Dict[str, str] = some_countries

                if data_request["command"] == "/bestdeal":
                    bot.set_state(message.from_user.id, RequestState.min_price, message.chat.id)
                else:
                    data_request["min_price"]: int = 1
                    data_request["max_price"]: int = 9999
                    bot.set_state(message.from_user.id, RequestState.year_incoming, message.chat.id)

            bot.send_message(message.chat.id, "Выберите место нахождения города:",
                             reply_markup=keyboards.list_countries(some_countries))
    else:
        bot.send_message(message.chat.id, "Введены неправильные данные! Введите название города!")


@bot.message_handler(state=RequestState.min_price)
def min_price(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает идентификатор города во внутренний словарь бота,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text in data_request["list_countries"]:
            data_request["id_city"]: str = data_request["list_countries"][message.text]
            bot.send_message(message.chat.id, "Введите минимальную цену бронирования за ночь(целое число) в $:")
            bot.set_state(message.from_user.id, RequestState.max_price, message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "Введены неправильные данные! Выберите местонахождение города из списка:",
                reply_markup=keyboards.list_countries(data_request["list_countries"])
            )


@bot.message_handler(state=RequestState.max_price)
def max_price(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает минимальную цену за ночь во внутренний словарь бота,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text.isdigit():
            data_request["min_price"]: str = message.text
            bot.send_message(message.chat.id, "Введите максимальную цену бронирования за ночь(целое число) в $:")
            bot.set_state(message.from_user.id, RequestState.min_distance, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Введены некорректные данные! Введите цену больше нуля!")


@bot.message_handler(state=RequestState.min_distance)
def min_distance(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает максимальную цену за ночь во внутренний словарь бота,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text.isdigit():
            if int(message.text) >= int(data_request["min_price"]):
                data_request["max_price"]: str = message.text
                bot.send_message(message.chat.id, "Введите минимальное расстояние от центра в км(формата 0.15)")
                bot.set_state(message.from_user.id, RequestState.max_distance, message.chat.id)
            else:
                bot.send_message(message.chat.id, "Максимальная цена должны быть больше или равна минимальной!")
        else:
            bot.send_message(message.chat.id, "Введены некорректные данные! Попробуйте еще раз!")


@bot.message_handler(state=RequestState.max_distance)
def max_distance(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных(до точки километры, после точки метры),
    записывает минимальное расстояние от центра в формате 0.15 км во внутренний словарь бота,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if fullmatch(r"\d+.\d{1,2}", message.text):
            data_request["min_distance"]: float = float(message.text)
            bot.send_message(message.chat.id, "Введите максимальное расстояние от центра в км(формата 0.15):")
            bot.set_state(message.from_user.id, RequestState.year_incoming, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Введены некорректные данные! Попробуйте еще раз!")


@bot.message_handler(state=RequestState.year_incoming)
def year_incoming(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных в зависимости от команды,
    записывает максимальное расстояние от центра в формате 0.15 км, идентификатор города во внутренний словарь бота и
    выводит для пользователя клавиатуру выбора года заезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if data_request["command"] != "/bestdeal":
            if message.text in data_request["list_countries"]:
                data_request["id_city"]: str = data_request["list_countries"][message.text]
                bot.set_state(message.from_user.id, RequestState.month_incoming, message.chat.id)
                data_request["list_years_income"]: List[str] = keyboards.years_buttons()
                reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_years_income"],
                                                                               "years")
                bot.send_message(message.chat.id, "Выберите год въезда в отель:", reply_markup=reply_markup)
            else:
                bot.send_message(
                    message.chat.id, "Введены неправильные данные! Выберите местонахождение города из списка:",
                    reply_markup=keyboards.list_countries(data_request["list_countries"])
                )
        else:
            if fullmatch(r"\d+.\d{1,2}", message.text):
                if float(message.text) >= data_request["min_distance"]:
                    data_request["max_distance"]: float = float(message.text)
                    bot.set_state(message.from_user.id, RequestState.month_incoming, message.chat.id)
                    data_request["list_years_income"]: List[str] = keyboards.years_buttons()
                    reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_years_income"],
                                                                                   "years")
                    bot.send_message(message.chat.id, "Выберите год въезда в отель:", reply_markup=reply_markup)
                else:
                    bot.send_message(message.chat.id,
                                     "Максимальное расстояние должно быть больше или равно минимальному!")
            else:
                bot.send_message(message.chat.id, "Введены некорректные данные! Попробуйте еще раз!")


@bot.message_handler(state=RequestState.month_incoming)
def month_incoming(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает год заезда в отель и выводит для пользователя клавиатуру выбора месяца заезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text in data_request["list_years_income"]:
            bot.set_state(message.from_user.id, RequestState.day_incoming, message.chat.id)
            data_request["year_incoming"]: str = message.text
            data_request["list_months_income"]: List[str] = keyboards.months_buttons(message.text)
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_months_income"], "months")
            bot.send_message(message.chat.id, "Выберите месяц въезда в отель:", reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Введены неправильные данные! Попробуйте еще раз!")


@bot.message_handler(state=RequestState.day_incoming)
def day_incoming(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает месяц заезда в отель и выводит для пользователя клавиатуру выбора дня заезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text.title() in data_request["list_months_income"]:
            bot.set_state(message.from_user.id, RequestState.year_out, message.chat.id)
            data_request["month_incoming"]: str = str(keyboards.dict_month_num[message.text.title()])
            data_request["list_days_income"]: List[str] = keyboards.days_buttons(in_month=message.text.title())
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_days_income"], "days")
            bot.send_message(message.chat.id, "Выберите день въезда в отель:", reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Введены неправильные данные!Попробуйте еще раз!")


@bot.message_handler(state=RequestState.year_out)
def year_out(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает день заезда в отель и выводит для пользователя клавиатуру выбора года отъезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text in data_request["list_days_income"]:
            bot.set_state(message.from_user.id, RequestState.month_out, message.chat.id)
            data_request["day_incoming"]: str = message.text
            data_request["list_years_outcome"]: List[str] = keyboards.years_buttons(
                chosen_year=data_request["year_incoming"], chosen_month=data_request["month_incoming"],
                chosen_day=data_request["day_incoming"])
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_years_outcome"], "years")
            bot.send_message(message.chat.id, "Выберите год отъезда из отеля:", reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Введены неправильные данные!Попробуйте еще раз!")


@bot.message_handler(state=RequestState.month_out)
def month_out(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает год отъезда в отель и выводит для пользователя клавиатуру выбора месяца отъезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text in data_request["list_years_outcome"]:
            bot.set_state(message.from_user.id, RequestState.day_out, message.chat.id)
            data_request["year_out"]: str = message.text
            data_request["list_months_outcome"]: List[str] = keyboards.months_buttons(
                in_year=data_request["year_incoming"], out_year=message.text,
                chosen_month=data_request["month_incoming"], chosen_day=data_request["day_incoming"])
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_months_outcome"],
                                                                           "months")
            bot.send_message(message.chat.id, "Выберите месяц отъезда из отеля:", reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Введены неправильные данные!Попробуйте еще раз!")


@bot.message_handler(state=RequestState.day_out)
def day_out(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает месяц отъезда в отель и выводит для пользователя клавиатуру выбора день отъезда,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text.title() in data_request["list_months_outcome"]:
            bot.set_state(message.from_user.id, RequestState.check_date, message.chat.id)
            data_request["month_out"]: str = str(keyboards.dict_month_num[message.text.title()])
            data_request["list_days_outcome"]: List[str] = keyboards.days_buttons(
                in_month=data_request["month_incoming"], chosen_day=data_request["day_incoming"],
                out_month=message.text.title())
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_days_outcome"], "days")
            bot.send_message(message.chat.id, "Выберите день отъезда из отеля:", reply_markup=reply_markup)
        else:
            bot.send_message(message.chat.id, "Введены неправильные данные!Попробуйте еще раз!")


@bot.message_handler(state=RequestState.check_date)
def check_date(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает день отъезда в отель и выводит вопрос уточнения дат пребывания в отеле,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
        if message.text in data_request["list_days_outcome"]:
            data_request["day_out"]: str = message.text
            info_date: List[str] = [data_request["year_incoming"], data_request["month_incoming"], data_request[
                "day_incoming"], data_request["year_out"], data_request["month_out"], data_request["day_out"]]
            update_date: List[str] = [f"0{i_elem}" if len(i_elem) == 1 else i_elem for i_elem in info_date]
            data_request["date_incoming"]: List[str] = [update_date[0], update_date[1], update_date[2]]
            data_request["date_outcoming"]: List[str] = [update_date[3], update_date[4], update_date[5]]
            bot.send_message(message.chat.id, f"Дата въезда: {'-'.join(data_request['date_incoming'])}\n"
                                              f"Дата выезда: {'-'.join(data_request['date_outcoming'])}\n\n"
                                              f"Все верно?(Да/Нет)", reply_markup=keyboards.markup)
            bot.set_state(message.from_user.id, RequestState.name_city, message.chat.id)
        else:
            bot.send_message(message.chat.id, "Ответ не понятен. Уточните, даты въезда верные?")


@bot.message_handler(state=RequestState.name_city)
def get_city(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    в зависимости от ответа пользователя предлагает ввести кол-во отелей, либо начать вводить даты пребывания снова,
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, "Выберите количество отелей, которое необходимо вывести в результате"
                                          "(Не больше пяти)", reply_markup=keyboards.buttons_numbers)
        bot.set_state(message.from_user.id, RequestState.amount_hotels, message.chat.id)
    elif message.text.lower() == "нет":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            data_request["list_years_income"]: List[str] = keyboards.years_buttons()
            reply_markup: ReplyKeyboardMarkup = keyboards.create_row_board(data_request["list_years_income"], "years")
            bot.send_message(message.chat.id, "Хорошо! Начнем с начала. Выберите год заезда:",
                             reply_markup=reply_markup)
            bot.set_state(message.from_user.id, RequestState.month_incoming, message.chat.id)
    else:
        bot.send_message(message.chat.id, "Введены неправильные данные!Попробуйте еще раз!")


@bot.message_handler(state=RequestState.amount_hotels)
def get_amount_hotels(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает кол-во отелей во внутренний словарь бота,
    спрашивает о неоходимости вывода фотографий и
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text in "12345":
        bot.send_message(message.chat.id, "Требуются ли вывод фотографий для каждого отеля?",
                         reply_markup=keyboards.markup)
        bot.set_state(message.from_user.id, RequestState.download_photos, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            data_request["amount_hotels"]: int = int(message.text)
    else:
        bot.send_message(message.chat.id, "Введены неправильные данные! Введите число отелей!(от 1 до 5)",
                         reply_markup=keyboards.buttons_numbers)


@bot.message_handler(state=RequestState.download_photos)
def get_photos(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает информацию о необходимости вывода фотографий и
    переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text.lower() == "да":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            data_request["download_photos"]: str = "Да"
        bot.send_message(message.chat.id, "Введите количество выводимых фотографий:(Не больше пяти)",
                         reply_markup=keyboards.buttons_numbers)
        bot.set_state(message.from_user.id, RequestState.amount_photos, message.chat.id)
    elif message.text.lower() == "нет":
        bot.set_state(message.from_user.id, RequestState.answer_request, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            data_request["amount_photos"]: int = 0
            data_request["download_photos"]: str = "Нет"
        check_final_apply_user(message)
    else:
        bot.send_message(
            message.chat.id, "Ошибка ввода. Просьба уточнить! Требуются ли вывод фотографий для каждого отеля?",
            reply_markup=keyboards.markup
        )


@bot.message_handler(state=RequestState.amount_photos)
def get_amount_photos(message: Message) -> None:
    """
    Функция проверяет сообщение пользователя на корректность введенных данных,
    записывает кол-во фотографий для вывода и переключает состояние для следующего хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text in "12345":
        bot.set_state(message.from_user.id, RequestState.answer_request, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            data_request["amount_photos"]: int = int(message.text)
        check_final_apply_user(message)
    else:
        bot.send_message(message.chat.id, "Введены неправильные данные! Введите число фотографий!(от 1 до 5)",
                         reply_markup=keyboards.buttons_numbers)
        bot.register_next_step_handler(message, get_amount_photos)


@bot.message_handler(content_types=["text"], state=RequestState.answer_request)
def answer_request(message: Message) -> None:
    """
    Функция уточняет корректность введенного запроса.
    Если ответ отрицательный, то предлагает ввести все данные сначала.
    Если ответ положительный, то собирает всю необходимую информацию в соответствии с запросом,
    выводит все собранные данные и записывает информацию о запросе в историю.
    Переключает состояние для стартового хендлера.
    :param message: Передается сообщение от пользователя
    :type message: Message
    """
    if message.text.lower() == "да":
        bot.send_message(message.chat.id, "Поиск займет около минуты! Ищу подходящие варианты...")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_request:
            array_hotels = get_data_hotels(
                id_town=data_request["id_city"], amount_hotels=data_request["amount_hotels"],
                start_booking=data_request["date_incoming"], finish_booking=data_request["date_outcoming"],
                amount_hotel_photos=data_request["amount_photos"], sorting=data_request["sorting"],
                min_price=data_request["min_price"], max_price=data_request["max_price"])

        list_name_hotels: str = ""

        for index, i_hotel in enumerate(array_hotels):
            if (data_request["command"] == "/bestdeal"
                and data_request["min_distance"] <= i_hotel[2] <= data_request["max_distance"]) \
                    or data_request["command"] in "/lowprice/highprice":

                if index == len(array_hotels) - 1:
                    list_name_hotels += f"{i_hotel[0]}"
                else:
                    list_name_hotels += f"{i_hotel[0]}, "

                bot.send_message(
                    message.chat.id, f"Название отеля: {i_hotel[0]}.\nАдрес отеля: {i_hotel[5][-1:]}.\n"
                                     f"Расстояние от центра: {i_hotel[1]} км.\nЦена за ночь: ${i_hotel[2]}.\n"
                                     f"Цена за указанные даты: {i_hotel[3]}.\n{i_hotel[4]}",
                    reply_markup=keyboards.help_keyboard)

                if len(i_hotel[5]) > 1:
                    bot.send_media_group(message.chat.id, i_hotel[5][:-1])

        if list_name_hotels == "":
            list_name_hotels = "Не найдено ни одного подходящего варианта!"
            bot.send_message(message.chat.id, list_name_hotels, reply_markup=keyboards.help_keyboard)

        db.add_information([data_request["command"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            data_request["name_city"].title(), list_name_hotels])
        bot.set_state(message.from_user.id, RequestState.command_start, message.chat.id)
    elif message.text.lower() == "нет":
        bot.set_state(message.from_user.id, RequestState.location_city, message.chat.id)
        bot.send_message(message.chat.id, "Все ошибаются! Начнем с начала! "
                                          "В каком городе хотите производить поиск отелей?")
    else:
        bot.send_message(message.chat.id, "Введены неправильные данные! Введите Да/Нет")


def register_handler() -> None:
    """ Функция передачи хендлера"""
    bot.register_message_handler(get_country, state=RequestState.location_city)
