from tbotAPI.create_bot import bot
from telebot import custom_filters


def main() -> None:
    """Запуск бота"""
    bot.add_custom_filter(custom_filter=custom_filters.StateFilter(bot=bot))
    bot.polling(non_stop=True, interval=0)


if __name__ == "__main__":
    main()
