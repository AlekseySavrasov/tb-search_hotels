import sqlite3
from typing import List


class Sqldb:
    def __init__(self) -> None:
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection: sqlite3.Connection = sqlite3.connect('telebot.db', check_same_thread=False)
        self.cursor: sqlite3.Cursor = self.connection.cursor()

        if self.connection:
            print('База данных подключена!')
        self.connection.execute("CREATE TABLE IF NOT EXISTS 'history' (command  VARCHAR(255), datetime DATETIME, "
                                "city VARCHAR(255), list_hotels VARCHAR(255))")
        self.connection.commit()

    def add_information(self, data_request: List[str]) -> sqlite3.Cursor.connection:
        """Добавление информации о команде поиска отелей в БД"""
        with self.connection:
            return self.cursor.execute("INSERT INTO 'history' VALUES(?, ?, ?, ?)",
                                       data_request).fetchall()

    def get_information(self) -> sqlite3.Cursor.connection:
        """Получение последних 10 записей из истории запросов"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'history' ORDER BY datetime DESC LIMIT 10").fetchall()

    def close(self) -> None:
        """Закрываем соединение с БД"""
        self.connection.close()


db: Sqldb = Sqldb()
