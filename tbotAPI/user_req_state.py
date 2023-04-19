from telebot.handler_backends import State, StatesGroup


class RequestState(StatesGroup):
    """
    Класс RequestState. Родитель: StatesGroup
    Содержит атрибуты состояний бота,
    которые переключаются в зависимости от определенных шагов выполнения handler'ов
    """
    command_start: State = State()
    min_price: State = State()
    max_price: State = State()
    min_distance: State = State()
    max_distance: State = State()
    year_incoming: State = State()
    month_incoming: State = State()
    day_incoming: State = State()
    year_out: State = State()
    month_out: State = State()
    day_out: State = State()
    check_date: State = State()
    name_city: State = State()
    location_city: State = State()
    amount_hotels: State = State()
    download_photos: State = State()
    amount_photos: State = State()
    answer_request: State = State()
