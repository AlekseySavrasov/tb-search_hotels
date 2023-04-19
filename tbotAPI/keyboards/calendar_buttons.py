from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
from typing import Optional, List, Union, Dict, Any


def check_date() -> datetime:
    """Функция возвращает текущее время и дату"""
    return datetime.now()


def create_row_board(list_row: List[Union[str, int]], type_size: str) -> ReplyKeyboardMarkup:
    """
    Функция создает клавиатуры для выбоа года, месяца, дня бронирования
    :param list_row: Передается список для создания клавиатуры
    :type list_row: List[Union[str, int]]
    :param type_size: Передается тип клавиатуры
    :type type_size: type_size: str
    :return: Возвращается клавиатура для выбора даты бронирования
    :rtype: ReplyKeyboardMarkup
    """
    years_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=10
    )
    months_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True,
        row_width=3
    )
    days_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        row_width=7
    )

    size_keyboards: Dict[str, ReplyKeyboardMarkup] = {
        "years": years_keyboard,
        "months": months_keyboard,
        "days": days_keyboard
    }

    a_row: List[KeyboardButton] = [KeyboardButton(i) for i in list_row]

    return size_keyboards[type_size].add(*a_row)


def years_buttons(chosen_year: Optional[Any] = None, chosen_month: Optional[Any] = None,
                  chosen_day: Optional[Any] = None) -> List[str]:
    """
    Функция создания списка годов бронирования в зависимости от переданных параметров
    :param chosen_year: Передается год заезда, дефолтное значение None
    :type chosen_year: Optional[Any]
    :param chosen_month: Передается месяц заезда, дефолтное значение None
    :type chosen_month: Optional[Any]
    :param chosen_day: Передается день заезда, дефолтное значение None
    :type chosen_day: Optional[Any]
    :return: Возвращается список возможных годов для бронирования
    :rtype: List[str]
    """
    if chosen_year is not None:

        if chosen_month == 12 and int(chosen_day) == 31:
            list_row: List[str] = [str(int(chosen_year) + 1 + num) for num in range(3)]
        else:
            list_row: List[str] = [str(int(chosen_year) + num) for num in range(3)]
    else:
        list_row: List[str] = [str(check_date().year + num) for num in range(3)]

    return list_row


def months_buttons(in_year: str, out_year: Optional[Any] = None, chosen_month: Optional[Any] = None,
                   chosen_day: Optional[Any] = None) -> List[str]:
    """
    Функция создания списка месяцев бронирования в зависимости от переданных параметров
    :param in_year: Передается год заезда в отель
    :type in_year: str
    :param out_year: Передается год выезда в отель, дефолтное значение None
    :type out_year: Optional[Any]
    :param chosen_month: Передается месяц заезда в отель, дефолтное значение None
    :type chosen_month: Optional[Any]
    :param chosen_day: Передается день заезда в отель, дефолтное значение None
    :type chosen_day: Optional[Any]
    :return: Возвращается список возможных месяцев для бронирования
    :rtype: List[str]
    """
    if out_year is None and int(in_year) == check_date().year:
        list_row: List[str] = [dict_month[month_num] for month_num in range(check_date().month, 13)]
    elif in_year == out_year:
        if int(chosen_day) == day_month[dict_month[int(chosen_month)]]:
            list_row: List[str] = [dict_month[month_num] for month_num in range(int(chosen_month) + 1, 13)]
        else:
            list_row: List[str] = [dict_month[month_num] for month_num in range(int(chosen_month), 13)]
    else:
        list_row: List[str] = [dict_month[month_num] for month_num in range(1, 13)]

    return list_row


def days_buttons(in_month: str, out_month: Optional[Any] = None, chosen_day: Optional[Any] = None) -> List[str]:
    """
    Функция создания списка дней бронирования в зависимости от переданных параметров
    :param in_month: Передается месяц заезда в отель
    :type in_month: str
    :param out_month: Передается месяц выезда из отеля, дефолтное значение None
    :type out_month: Optional[Any]
    :param chosen_day: Передается день заезда в отель, дефолтное значение None
    :type chosen_day: Optional[Any]
    :return: Возвращается список возможных дней для бронирования
    :rtype: List[str]
    """
    if out_month is None:
        end_month: int = day_month[in_month] + 1

        if dict_month_num[in_month] == check_date().month:
            list_row: List[str] = [str(day_num) for day_num in range(check_date().day, end_month)]
        else:
            list_row: List[str] = [str(day_num) for day_num in range(1, end_month)]

    else:
        end_month: int = day_month[out_month] + 1

        if in_month == str(dict_month_num[out_month]):
            list_row: List[str] = [str(day_num) for day_num in range(int(chosen_day) + 1, end_month)]
        else:
            list_row: List[str] = [str(day_num) for day_num in range(1, end_month)]

    return list_row


dict_month_num: Dict[str, int] = {
    "Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4, "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8, "Сентябрь": 9,
    "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12
}

day_month: Dict[str, int] = {
    "Январь": 31, "Февраль": 28, "Март": 31, "Апрель": 30, "Май": 31, "Июнь": 30, "Июль": 31, "Август": 31,
    "Сентябрь": 30, "Октябрь": 31, "Ноябрь": 30, "Декабрь": 31
}

dict_month: Dict[int, str] = {
    1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь", 7: "Июль", 8: "Август", 9: "Сентябрь",
    10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"
}
