from settings import site
from typing import Dict, Union, List

main_url: str = site.rapid_api_host

headers: Dict[int, Dict[str, str]] = {
    1: {
        "X-rapidAPI-Key": site.rapid_api_key.get_secret_value(),
        "X-rapidAPI-Host": main_url
    },
    2: {
        "content-type": "application/json",
        "X-rapidAPI-Key": site.rapid_api_key.get_secret_value(),
        "X-rapidAPI-Host": site.rapid_api_host
    }
}

methods: Dict[int, str] = {
    1: "GET",
    2: "POST"
}

urls: Dict[int, str] = {
    1: f"https://{main_url}/locations/v3/search",
    2: f"https://{main_url}/properties/v2/list",
    3: f"https://{main_url}/properties/v2/detail"
}


def create_qs(id_city) -> Dict[str, str]:
    """Функция собирает и возвращает информацию в требуемом формате для запроса локации искомых городов
    """
    return {"q": id_city, "locale": "ru_RU"}


def create_pl_data_hotels(id_town: str, start: List[str], finish: List[str], amount_hotels: int, order: str,
                          min_price: int, max_price: int) -> Dict[str, Union[str, int, Dict[str, Union[int, str]]]]:
    """Функция собирает и возвращает информацию в требуемом формате для запроса поиска отелей в искомом городе"""
    return {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": id_town},
            "checkInDate": {
                "day": int(start[2]),
                "month": int(start[1]),
                "year": int(start[0])
            },
            "checkOutDate": {
                "day": int(finish[2]),
                "month": int(finish[1]),
                "year": int(finish[0])
            },
            "rooms": [
                {
                    "adults": 1
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": amount_hotels,
            "sort": order,
            "filters": {"price": {
                "max": max_price,
                "min": min_price
            }}
        }


def create_pl_hotel_detail(id_hotel: str) -> Dict[str, Union[str, int]]:
    """Функция собирает и возвращает информацию в требуемом формате для запроса деталей оп искомым отелям"""
    return {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": id_hotel
        }
