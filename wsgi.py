from flask import Flask, render_template, request
from datetime import datetime


from models import Monitoring
from web_form import TimeSelectForm
import config
from web_tools import *


app = Flask(__name__)  # обьект нашего сервера
app.config['SECRET_KEY'] = config.SECRET_KEY


@app.route('/', methods=('GET', 'POST'))
def select():
    form = TimeSelectForm()  # экземпляр нашей формы

    if request.method == 'POST' and form.validate_on_submit():  # Если метод запроса - POST и если поля формы валидны
        # вытаскиваем временные переменные
        start = (request.form.get('start_time'))
        end = (request.form.get('end_time'))
        print(f"Начало: {start} - Конец: {end}")  # check
        # доп.проверка на логичность
        if datetime.strptime(start, '%Y-%m-%d %H:%M:%S') > datetime.now() or \
                datetime.strptime(end, '%Y-%m-%d %H:%M:%S') < datetime.strptime(start, '%Y-%m-%d %H:%M:%S'):
            return f"Некорректно задан диапазон"
        # вытаскиваем данные из бд за необходимый временной промежуток
        select_data = Monitoring.select().where(Monitoring.up_date >= start).where(Monitoring.up_date <= end)
        if not select_data:  # если пусто
            return "Извините но за данный временной промежуток отсутствуют данные"
        # подготавливаем данные к отправки в шаблонизатор
        column = []  # столбцы
        data = []  # данные для заполнения столбцов
        # смотрим какие данные нас интересуют и фиксируем это
        for sensor in config.ACTUAL_SENSOR:
            get_sensor = request.form.get(sensor)
            if get_sensor:
                column.append(sensor)
        print(f'Need sensor data: {column}')  # check
        # подготовка необходимых данных
        for row in select_data:
            temp = [row.__dict__['__data__']['up_date']]
            for col in column:
                temp.append(row.__dict__['__data__'][col])
            data.append(temp)
        # всё в порядке, данные подготовлены, отображаем таблицу
        return render_template('arduino.html', data=data, column=column)

    data = list(Monitoring.select()[0].__dict__['__data__'].keys())[1:-1]  # имена столбцов из бд, для checkbox'сов
    print(f'Your sensor: {data}')  # check
    return render_template('select.html', form=form, data=data)  # страница для получение данных от пользователя


@app.after_request
def add_header(r):
    """что бы избавиться от кеширования"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run()  # запуск сервера
