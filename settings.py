from os import getenv
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    """Класс SiteSettings. Родитель: BaseSettings.
    Содержит атрибуты в которых хранится информация о скрытых данных из среды окружения

    Attributes:
        rapid_api_key (SecretStr): токен для взаимодействия с rapidAPI
        rapid_api_host (StrictStr): сайт хоста rapidAPI
        bot_token (SecretStr): токен для взаимодействия с telegamAPI
    """
    rapid_api_key: SecretStr = getenv("RapidAPI_Key", None)
    rapid_api_host: StrictStr = getenv("RapidAPI_Host", None)
    bot_token: SecretStr = getenv("Token_Telebot", None)


site: SiteSettings = SiteSettings()
