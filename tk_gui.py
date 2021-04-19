import tkinter as TK  # всё необходимое для создания графического интерфейса
from tkinter import messagebox  # messagebox.showinfo('TEXT')
from PIL import Image, ImageTk
from _tkinter import TclError
from asyncio import sleep, get_event_loop, gather  # для асинхронного выполнения задач


from config import SPEEDS
from arduino_func import serial_ports


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

# лейблы
ports_label = TK.Label(text='Выберите порт:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # порты
speed_label = TK.Label(text='Выберите скорость:', width=20,
                       font=("Arial Bold", 24), bg="CadetBlue1", fg="gray1")  # скорости
info_label = TK.Label(width=50, height=7, font=("Arial Bold", 24), textvariable=logging_info,
                      bg="CadetBlue1", fg="gray1")  # информирование о последних записях

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
info_label.pack()


# функции для кнопок
def start():
    """начинаем опрашивать arduino и писать данные в бд"""
    select_ports = ports.get()
    select_speed = speed.get()
    if select_ports and select_speed:
        print(select_ports, select_speed)
        start_button['state'] = 'disabled'
        stop_button['state'] = 'normal'
    else:
        pass


def stop():
    """останавливаем программу"""
    stop_button['state'] = 'disabled'
    start_button['state'] = 'normal'


start_button['command'] = start
stop_button['command'] = stop


# Запуск приложения
async def gui():
    while True:
        try:
            root_window.update_idletasks()
            root_window.update()
        except TclError:
            raise KeyboardInterrupt
        else:
            await sleep(0.01)


async def work_with_async():  # наши асинхронные задачи
    await gather(gui())  # передаем очередь на выполнение


if __name__ == "__main__":
    stop_button['state'] = 'disabled'
    loop = get_event_loop()  # цикл отслеживающий асинхронные задачи
    loop.run_until_complete(work_with_async())  # где отслеживаем

