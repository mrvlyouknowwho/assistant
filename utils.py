""" Вспомогательные функции """
import socket
import random
from exceptions import InternetConnectionError

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        print("Дебаг: Соединение с интернетом есть.")
        return True
    except socket.error as e:
        print(f"Дебаг: Нет соединения с интернетом: {e}")
        raise InternetConnectionError(f"No internet connection: {e}")

def fix_errors():
    print("Дебаг: Исправление ошибок...")
    print("Ассистент: Пытаюсь исправить ошибки...")
    print("Ассистент: Может попробуем другой запрос?")
    print("Дебаг: Исправление ошибок завершено.")

def add_function():
    print("Дебаг: Добавление функции...")
    print("Ассистент: Пытаюсь добавить новую функцию...")
    print("Ассистент: Я работаю над этим!")
    print("Дебаг: Добавление функции завершено.")