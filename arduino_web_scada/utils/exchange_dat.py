"""Для обмена данными между модулями с целью избежания цикличных импортов"""
import shelve


FILENAME = "arduino_web_scada/utils/exchange"  # файл где хранятся данные для обмена


ser = None  # будущий коннект


def shelve_write(var: str, value):
    """сохранение данных"""
    with shelve.open(FILENAME) as file:
        file[var] = value


def shelve_read(var: str):
    """считывание данных"""
    with shelve.open(FILENAME) as file:
        return file[var]


def save_ser(connect):
    """сохраняем соединение"""
    global ser
    ser = connect


def load_ser():
    """выгружаем соединение"""
    global ser
    return ser
