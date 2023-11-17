To work with the bot, you need:

1. Clone the remote repository to your local computer (git remote add :).
2. Install the necessary libraries through the terminal (pip install -r requirements.txt).
3. Telegram must be installed on user devices.
4. Launch the Telegram bot with the command python main.py from the terminal — from the folder with the Telegram bot.
5. To deploy the application, you can use a Dockerfile.

Information on Telegram bot commands:

1. Command /start: After entering the command, it displays the initial informational message.
2. Command /help: After entering the command, it displays a list of existing commands and their descriptions.
3. Command /lowprice: The command displays the top cheapest hotels in the city. After entering the command, the user is prompted for:
The city where the search will take place.
The number of hotels to display in the result (not exceeding a predetermined maximum).
The need to download and display photos for each hotel ("Yes/No"). When answering "Yes," the user also enters the number of photos needed (not exceeding a predetermined maximum).
4. Command /highprice: The command displays the top most expensive hotels in the city. After entering the command, the user is prompted for:
The city where the search will take place.
The number of hotels to display in the result (not exceeding a predetermined maximum).
The need to download and display photos for each hotel ("Yes/No"). When answering "Yes," the user also enters the number of photos needed (not exceeding five).
5. Command /bestdeal: The command displays hotels that are suitable in terms of price and location from the center within a range. After entering the command, the user is prompted for:
The city where the search will take place.
Price range.
The range of distance at which the hotel is located from the center.
The number of hotels to display in the result (not exceeding a predetermined maximum).
The need to download and display photos for each hotel ("Yes/No"). When answering "Yes," the user also enters the number of photos needed (not exceeding five).
6. Command /history: After entering the command, the user is shown the search history of hotels (the last ten queries). The history itself includes:
The command entered by the user.
The date and time of entering the command.
The city where hotel search was performed.
The hotels that were found.


Для работы с ботом требуется:

1. Клонирование удаленного репозитория на локальный компьютер
(git remote add <shortname> <url>:).
2. Установка необходимых библиотек через терминал (pip install -r requirements.txt)
3. Должен быть установлен Telegram на устройствах пользования.
4. Запуск Telegram-бота выполняется командой python main.py из терминала — из
папки с Telegram-ботом.
5. Развернуть приложение можно через Dockerfile

Информация по командам Telegram-бота:

1. Команда /start
После ввода команды выводит стартовое информационное сообщение.
2. Команда /help
После ввода команды выводит список существующих команд и их описание.
3. Команда /lowprice
Команда выводит топ самых дешёвых отелей в городе.
После ввода команды у пользователя запрашивается:
   1. Город, где будет проводиться поиск.
   2. Количество отелей, которые необходимо вывести в результате (не больше
   заранее определённого максимума).
   3. Необходимость загрузки и вывода фотографий для каждого отеля («Да/Нет»):
   4. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше заранее определённого
   максимума).

4. Команда /highprice
Команда выводит топ самых дорогих отелей в городе.
После ввода команды у пользователя запрашивается:
   1. Город, где будет проводиться поиск.
   2. Количество отелей, которые необходимо вывести в результате (не больше
   заранее определённого максимума).
   3. Необходимость загрузки и вывода фотографий для каждого отеля («Да/Нет»):
   4. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше пяти).

5. Команда /bestdeal
Команда выводит отели подходящие по цене и расположению от центра в диапазоне.
После ввода команды у пользователя запрашивается:
   1. Город, где будет проводиться поиск.
   2. Диапазон цен.
   3. Диапазон расстояния, на котором находится отель от центра.
   4. Количество отелей, которые необходимо вывести в результате (не больше
   заранее определённого максимума).
   5. Необходимость загрузки и вывода фотографий для каждого отеля («Да/Нет»):
   6. При положительном ответе пользователь также вводит количество
   необходимых фотографий (не больше пяти).

6. Команда /history
После ввода команды пользователю выводится история поиска отелей(последние
десять запросов). Сама история содержит:
   1. Команду, которую вводил пользователь.
   2. Дату и время ввода команды.
   3. Город поиска отелей
   4. Отели, которые были найдены.