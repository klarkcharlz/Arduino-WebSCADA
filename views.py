"""наши представления"""
from flask import render_template, request

from web_form import TimeSelectForm  # наши формы
from logging_config import logger  # наше логирование
from server_func import (clear_cache, get_date, valid_time_period, select_db,
                         data_preparation_for_table, get_column_name,
                         data_preparation_for_trend)  # доп.функции


def select():
    form = TimeSelectForm()  # экземпляр нашей формы

    if request.method == 'POST' and form.validate_on_submit():  # Если метод запроса - POST и если поля формы валидны
        # вытаскиваем временные переменные
        start, end = get_date(request)
        # доп.проверка на логичность
        if not valid_time_period(start, end):
            return f"Некорректно задан диапазон"
        # вытаскиваем данные из бд за необходимый временной промежуток
        select_data = select_db(start, end)
        if not select_data:  # если пусто
            logger.error(f"Данные за запрошенный период отсутствуют")
            return "Извините но за данный временной промежуток отсутствуют данные"
        # определяем вид визуализации таблица или тренд и подготавливаем данные к отправки в шаблонизатор
        if request.form.get('vizual_type') == 'table':
            data, column = data_preparation_for_table(request, select_data)
            return render_template('arduino_table.html', data=data, column=column)
        elif request.form.get('vizual_type') == 'trend':
            data, date = data_preparation_for_trend(request, select_data)
            print(data)
            return render_template('arduino_trend.html', data=data, start=start, end=end, date=date)
        else:
            return "OOPS!"

    data = get_column_name()  # имена столбцов из бд, для checkbox'сов
    return render_template('select.html', form=form, data=data)  # страница для получение данных от пользователя


def add_header(r):
    return clear_cache(r)


def test_calender():
    """Работаем над календарем"""
    return render_template('test/test_calender.html')


def test_trend():
    """Работаем над трендом"""
    data = [1, 2, 3, 4, 5, 6, 6, 6, 5, 4, 3, 2, 1]
    from datetime import datetime
    time = [datetime.now() for _ in range(13)]  # для оси Y
    time = [date.strftime('%Y/%m/%d %H:%M:%S') for date in time]  # для оси X
    return render_template('test/test_date.html', time=time, data=data)
