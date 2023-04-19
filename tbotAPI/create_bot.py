from telebot import TeleBot
from settings import site


bot: TeleBot = TeleBot(site.bot_token.get_secret_value())
