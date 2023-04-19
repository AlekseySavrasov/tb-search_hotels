from telebot.types import ReplyKeyboardMarkup
from typing import Dict


def list_countries(array_countries: Dict[str, str]) -> ReplyKeyboardMarkup:
    """
    Функция создания клавиатуры для выбора страны нахождения города
    :param array_countries: Передается словарь со странами нахождения города
    :type array_countries: Dict[str, str]
    :return: Возвращается клавиатура с кнопками стран возможного нахождения искомого города
    :rtype: ReplyKeyboardMarkup
    """
    buttons_countries: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    for i_country in array_countries:
        buttons_countries.add(i_country)

    return buttons_countries


markup: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
help_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
button_help: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
buttons_numbers: ReplyKeyboardMarkup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

markup.add("Да", "Нет")
button_help.add("/help")
buttons_numbers.add("1", "2", "3", "4", "5")
help_keyboard.add("/lowprice", "/highprice", "/bestdeal", "/history")
