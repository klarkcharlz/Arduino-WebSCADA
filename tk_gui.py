import tkinter as TK  # всё необходимое для создания графического интерфейса
from tkinter import messagebox  # messagebox.showinfo('TEXT')
from PIL import Image, ImageTk
from _tkinter import TclError
from asyncio import sleep, gather  # для асинхронного выполнения задач
import serial  # для работы с портом
import time  # для задержки


# наши модули
from config import SPEEDS  # скорости обмена данными
from arduino_func import serial_ports, find_arduino  # дополнительные функции
from arduino_control import arduino_data_read  # функция чтения и записи данных
from logging_config import logger  # логирование


ser = None  # будущий коннект
flag = False  # флаг запущенного соединения

# создадим графический интерфейс
root_window = TK.Tk()  # главное окно
root_window.title('Arduino Client')  # заголовок окна
root_window.geometry("1080x720+600+200")  # задаем размеры окна + задаем смещение появление окна относительно экрана

# фон
img = Image.open("./static/img/deckope.png")  # Открываем картинку
img = img.resize((1080, 720))  # Изменяем размер картинки
background_img = ImageTk.PhotoImage(img)  # Создаём PhotoImage
# создаем фон как обьект Label и помещаем его в окно
background_label = TK.Label(root_window, image=background_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# переменные
ports = TK.StringVar(root_window)  # порты
speed = TK.StringVar(root_window)  # скорости
logging_info = TK.StringVar(root_window)  # информирование о последних записях
speed.set(SPEEDS[3])  # по умалчиванию 9600
try:
    ports.set(find_arduino())  # пытаемся установить порт по умалчиванию с автоопределением подключенного Arduino
    logger.info(f"Arduino обнаружен на порту: {ports.get()}")
except Exception as err:
    logger.info(f'Не удалось обнаружить Arduino. {type(err)}: {err}.')

# лейблы
ports_label = TK.Label(text='Выберите порт:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # порты
speed_label = TK.Label(text='Выберите скорость:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # скорости
log_label = TK.Label(width=150, height=20, font=("Arial Bold", 12),
                     bg="CadetBlue1", fg="gray1", textvariable=logging_info)  # актуальный лог

# выпадающие списки
ports_list = TK.OptionMenu(root_window, ports, *serial_ports())  # порты
speed_list = TK.OptionMenu(root_window, speed, *SPEEDS)  # скорости
ports_list.config(width=21, font=("Arial Bold", 20), bg="CadetBlue1", fg="gray1")
speed_list.config(width=21, font=("Arial Bold", 20), bg="CadetBlue1", fg="gray1")


# кнопки
start_button = TK.Button(root_window, text='Старт', width=20, height=3, bg="CadetBlue1", fg="gray1")  # старт
stop_button = TK.Button(root_window, text='Стоп', width=20, height=3, bg="CadetBlue1", fg="gray1")  # стоп

# распологаем виджеты
ports_label.pack()
ports_list.pack()
speed_label.pack()
speed_list.pack()
start_button.pack()
stop_button.pack()
log_label.pack()


# функции для кнопок
def start():
    """начинаем опрашивать arduino и писать данные в бд"""
    select_ports = ports.get()  # получаем данные для соединения
    select_speed = speed.get()
    if select_ports and select_speed:  # если всё необходимое есть стартуем соединение
        start_button['state'] = 'disabled'  # делаем кнопку старт неактивной
        stop_button['state'] = 'normal'
        global ser
        ser = serial.Serial(select_ports, baudrate=select_speed, timeout=1)  # создаем соединение
        logger.info(f'Старт соединения. Порт: {select_ports}. Скорость: {select_speed}')  # фиксируем подключение
        gather(arduino_data_read())  # начинаем работу
        time.sleep(3)  # немного подождем
        global flag  # флаг активного соединения
        flag = True
    else:  # если данных нет
        pass


def stop():
    """останавливаем соединение"""
    stop_button['state'] = 'disabled'  # делаем кнопку стоп неактивной
    start_button['state'] = 'normal'
    ser.close()  # стоп соединения
    global flag
    flag = False  # флаг активного соединения
    logger.info(f'Закрываем соединение')  # фиксируем отключение
    time.sleep(3)  # немного подождем


# назначаем функции на кнопки
start_button['command'] = start
stop_button['command'] = stop


# Запуск приложения
async def gui():
    while True:
        try:
            # обновляем интерфейс
            root_window.update_idletasks()
            root_window.update()
            with open("./log/arduinoWebScada.log", 'r') as f:
                text = f.readlines()
                logging_info.set("".join(text[-18:]))
        except TclError:
            raise KeyboardInterrupt
        else:
            await sleep(0.01)


stop_button['state'] = 'disabled'  # первоначально кнопка неактивна
