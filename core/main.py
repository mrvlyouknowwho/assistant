""" Основной файл запуска ассистента """
import time
import random
import os

from assistant.data.database import Database
from assistant.core.dispatcher import Dispatcher
from assistant.utils import check_internet_connection
from assistant.config import DATABASE_PATH
from assistant.exceptions import InternetConnectionError


def main():
    print("Дебаг: Запуск ассистента...")
    try:
        db = Database(DATABASE_PATH)
        dispatcher = Dispatcher(db)
    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        return

    if not check_internet_connection():
        print ("Ассистент: Нет соединения с интернетом.")
        return

    while True:
       try:
           dispatcher.process_query()
       except Exception as e:
           print (f"Ошибка при обработке запроса: {e}")
           continue

    print("Дебаг: Ассистент завершил работу.")


if __name__ == "__main__":
    main()