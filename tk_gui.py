import tkinter as TK  # всё необходимое для создания графического интерфейса
from tkinter import messagebox  # messagebox.showinfo('TEXT')
from PIL import Image, ImageTk
from _tkinter import TclError  # обновление при закрытии окна
from asyncio import sleep, gather  # для асинхронного выполнения задач
import serial  # для работы с портом
import time  # для задержки
import webbrowser  # для открытия сервера в браузере


# наши модули
from config import SPEEDS  # скорости обмена данными
from arduino_func import serial_ports, find_arduino  # дополнительные функции
from arduino_control import arduino_data_read  # функция чтения и записи данных
from logging_config import logger  # логирование
import run_server  # для управления сервером


ser = None  # будущий коннект
flag = False  # флаг запущенного соединения
log_active = False  # статус окна логов

# создадим графический интерфейс
root_window = TK.Tk()  # главное окно
root_window.title('Arduino Client')  # заголовок окна
root_window.geometry("1080x720+200+100")  # задаем размеры окна + задаем смещение появление окна относительно экрана

# переменные
ports = TK.StringVar(root_window)  # порты
speed = TK.StringVar(root_window)  # скорости
speed.set(SPEEDS[3])  # по умалчиванию 9600


# меню
def logs():
    """Актуальные логи"""
    def on_closing():
        """обработчик закрытия окна логов"""
        global log_active
        log_active = False  # фиксируем закрытие окна логов
        log_window.destroy()

    global log_active
    log_active = True  # фиксируем открытие окна логов
    log_window = TK.Tk()  # главное окно
    log_window.protocol("WM_DELETE_WINDOW", on_closing)  # обработка закрытия окна логов
    log_window.title('Arduino Client log')  # заголовок окна
    log_window.geometry("1000x600+200+100")  # задаем размеры окна + задаем смещение появление окна относительно экрана
    logging_info = TK.StringVar(log_window)  # Переменная для информирование о последних записях
    log_label = TK.Label(log_window, width=150, font=("Arial Bold", 12),
                         bg="CadetBlue1", fg="gray1", textvariable=logging_info)  # актуальный лог
    log_label.pack()

    async def update_log():
        """Обновление логов"""
        while True:
            if not log_active:  # проверяем открыто ли окно, если нет прекращаем выполнение функции
                break
            with open("./log/arduinoWebScada.log", 'r') as f:
                # читаем актуальные логи
                text = f.readlines()
                logging_info.set("".join(text[-30:]))
            await sleep(0.5)
    gather(update_log())


main_menu = TK.Menu()
root_window.config(menu=main_menu)
main_menu.add_command(label='Логи', command=logs)

# фон
img = Image.open("./static/img/deckope.png")  # Открываем картинку
img = img.resize((1080, 720))  # Изменяем размер картинки
background_img = ImageTk.PhotoImage(img)  # Создаём PhotoImage
# создаем фон как обьект Label и помещаем его в окно
background_label = TK.Label(root_window, image=background_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

try:
    # пытаемся установить порт по умалчиванию с автоопределением подключенного Arduino
    default_port = find_arduino()
    if default_port != "None":
        ports.set(default_port)
        logger.info(f"Arduino обнаружен на порту: {ports.get()}")
except Exception as err:
    logger.info(f'Не удалось обнаружить Arduino. {type(err)}: {err}.')

# лейблы
ports_label = TK.Label(root_window, text='Выберите порт:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # порты
speed_label = TK.Label(root_window, text='Выберите скорость:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # скорости


# выпадающие списки
ports_list = TK.OptionMenu(root_window, ports, *serial_ports())  # порты
speed_list = TK.OptionMenu(root_window, speed, *SPEEDS)  # скорости
ports_list.config(width=21, font=("Arial Bold", 20), bg="CadetBlue1", fg="gray1")
speed_list.config(width=21, font=("Arial Bold", 20), bg="CadetBlue1", fg="gray1")


# кнопки
start_button = TK.Button(root_window, text='Старт', width=20, height=3, bg="CadetBlue1", fg="gray1")
stop_button = TK.Button(root_window, text='Стоп', width=20, height=3, bg="CadetBlue1", fg="gray1")
server_start = TK.Button(root_window, text='Запустить сервер', width=20, height=3, bg="CadetBlue1", fg="gray1")
server_stop = TK.Button(root_window, text='Остановить сервер', width=20, height=3, bg="CadetBlue1", fg="gray1")
open_server = TK.Button(root_window, text='Открыть', width=20, height=3, bg="CadetBlue1", fg="gray1")

# распологаем виджеты
ports_label.place(relx=0.33, rely=0.0)
ports_list.place(relx=0.33, rely=0.06)
speed_label.place(relx=0.33, rely=0.12)
speed_list.place(relx=0.33, rely=0.18)

start_button.place(relx=0.33, rely=0.25)
stop_button.place(relx=0.53, rely=0.25)

server_start.place(relx=0.33, rely=0.45)
server_stop.place(relx=0.53, rely=0.45)
open_server.place(relx=0.43, rely=0.55)


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


def start_server():
    """Запуск сервера"""
    logger.info('Запуск сервера')
    run_server.start_server()  # запуск сервера
    # меняем статус кнопок
    server_stop['state'] = 'normal'
    open_server['state'] = 'normal'
    server_start['state'] = 'disabled'


def stop_server():
    """Остановка сервера"""
    logger.info('Остановка сервера')
    run_server.stop_server()  # остановка сервера
    # меняем статус кнопок
    server_stop['state'] = 'disabled'
    open_server['state'] = 'disabled'
    server_start['state'] = 'normal'


def open_server_func():
    webbrowser.get(using='opera').open_new_tab('http://127.0.0.1:5000/')


# назначаем функции на кнопки
start_button['command'] = start
stop_button['command'] = stop
server_start['command'] = start_server
server_stop['command'] = stop_server
open_server['command'] = open_server_func


# Запуск приложения
async def gui():
    """рисуем графический интерфейс"""
    while True:
        # обновляем интерфейс
        try:
            root_window.update_idletasks()
            root_window.update()
        except TclError:  # для завершения приложения в случае закрытия главного окна
            raise KeyboardInterrupt
        else:
            await sleep(0.01)


# первоначальные состояния кнопок
stop_button['state'] = 'disabled'
server_stop['state'] = 'disabled'
open_server['state'] = 'disabled'
