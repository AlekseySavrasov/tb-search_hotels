from telebot import TeleBot
from os import getenv

bot_token = getenv('TOKEN')
bot: TeleBot = TeleBot(bot_token)
