from telebot import types
from requests import request, Response
from typing import List, Dict, Optional, Union, Any
from rapidAPI import core
import json


def check_answer(req_answer: int) -> bool:
    """
    Функция проверки ответа сайта
    :param req_answer: Передается статус-код ответа сайта
    :type req_answer: int
    :return: Возвращается False или True после сравнения req_answer c 200
    :rtype: bool
    """
    if req_answer == 200:
        return True
    else:
        return False


def response_request(
        method: str, url: str, headers: Dict[str, str], querystring: Optional[Any] = None,
        payload: Optional[Any] = None) -> Union[int, Response]:
    """
    Функция создания запроса для получения информации через rapidAPI
    :param method: Передается метод запроса
    :type method: str
    :param url: Передается url запроса
    :type url: str
    :param headers: Передается headers запроса
    :type headers: Dict[str, str]
    :param querystring: Передается querystring запроса
    :type querystring: Optional[Any]
    :param payload: Передается payload запроса
    :type payload: Optional[Any]
    :return: Возвращается полностью собранный запрос
    :rtype: Response
    """
    response: Response = request(
        method=method,
        url=url,
        headers=headers,
        params=querystring,
        json=payload
    )

    return response


def get_data_city(a_city: str) -> Dict[str, str]:
    """
    Функция получения информации о возможном нахождении искомого города
    :param a_city: Передается id искомого города
    :type a_city: str
    :return: Возвращается словарь с возможными локациями города и его id
    :rtype: Dict[str, str]
    """
    list_city_id: Dict = {}

    info_request: Response = response_request(
        method=core.methods[1],
        url=core.urls[1],
        headers=core.headers[1],
        querystring=core.create_qs(
            id_city=a_city
        )
    )

    if check_answer(info_request.status_code):
        data_request: json = json.loads(info_request.text)

        for country_item in data_request["sr"]:
            if country_item["type"] == "CITY":
                id_city: str = country_item["gaiaId"]
                country_city: str = country_item["regionNames"]["fullName"]
                list_city_id[country_city]: str = id_city

    return list_city_id


def get_data_hotels(
        id_town: str, amount_hotels: int, start_booking: List[str], finish_booking: List[str], amount_hotel_photos: int,
        sorting: str, min_price: int, max_price: int) -> List[List[Optional[Any]]]:
    """
    Функция получения отелей находящихся в искомом городе в соответствии с введенными условиями
    :param id_town: Передается идентификатор города
    :type id_town: str
    :param amount_hotels: Передается кол-во отелей для поиска
    :type amount_hotels: int
    :param start_booking: Передается дата въезда в отель
    :type start_booking: List[str]
    :param finish_booking: Передается дата выезда из отеля
    :type finish_booking: List[str]
    :param amount_hotel_photos: Передается кол-во фотографий для
    :type amount_hotel_photos: int
    :param sorting: Передается тип сортировки найденных отелей
    :type sorting: str
    :param min_price: Передается желаемая минимальная цена бронирования за ночь
    :type max_price: int
    :param max_price: Передается желаемая максимальная цена бронирования за ночь
    :type min_price: int
    :return: Возвращается список найденных отелей с необходимой информацией:
    имя отеля, расстояние от центра, цена за ночь, цена за весь период бронирования, сайт отеля, список(фото. адрес)
    :rtype: List[List[Optional[Any]]]
    """
    list_hotels: List[List] = []
    info_request: Response = response_request(
            method=core.methods[2],
            url=core.urls[2],
            headers=core.headers[2],
            payload=core.create_pl_data_hotels(
                id_town=id_town,
                start=start_booking,
                finish=finish_booking,
                amount_hotels=amount_hotels,
                order=sorting,
                min_price=min_price,
                max_price=max_price
            )
        )

    if check_answer(info_request.status_code):
        data_request: json = json.loads(info_request.text)

        for hotel_num in range(amount_hotels):
            root_path: Dict = data_request["data"]["propertySearch"]["properties"]

            hotel_id: str = root_path[hotel_num]["id"]
            hotel_name: str = root_path[hotel_num]["name"]
            range_to_center: str = root_path[hotel_num]["destinationInfo"]["distanceFromDestination"]["value"]
            total_price: str = root_path[hotel_num]["price"]["displayMessages"][1]["lineItems"][0]["value"]
            night_price: int = root_path[hotel_num]["price"]["lead"]["amount"]
            hotel_url: str = f'https://www.hotels.com/h{hotel_id}.Hotel-Information'
            list_details: List[str] = get_hotel_detail(hotel_id=hotel_id, amount_photos=amount_hotel_photos)

            info_about_hotel: List[Optional[Any]] = [hotel_name, range_to_center, night_price, total_price,
                                                     hotel_url, list_details]
            list_hotels.append(info_about_hotel)

    return list_hotels


def get_hotel_detail(hotel_id: str, amount_photos: int) -> List[str]:
    """
    Функция получения адреса отеля и прилагаемых к нему фотографий
    :param hotel_id: Передается идентификатор отеля
    :type hotel_id: str
    :param amount_photos: Передается желаемое кол-во выводимых фотографий
    :type amount_photos: int
    :return: Возвращается список фотографий и адреса отеля
    :rtype: List[str]
    """
    array_details: List[str] = []
    info_request: Response = response_request(
            method=core.methods[2],
            url=core.urls[3],
            headers=core.headers[2],
            payload=core.create_pl_hotel_detail(id_hotel=hotel_id)
        )

    if check_answer(info_request.status_code):
        data_details: json = json.loads(info_request.text)
        root_path: Dict[Any] = data_details["data"]["propertyInfo"]

        if amount_photos != 0:
            for num_photo in range(amount_photos):
                link_of_photo: str = root_path["propertyGallery"]["images"][num_photo]["image"]["url"]
                url_photo: str = link_of_photo.replace("{size}", "w")
                array_details.append(types.InputMediaPhoto(url_photo))

        array_details.append(root_path["summary"]["location"]["address"]["addressLine"])

    return array_details
