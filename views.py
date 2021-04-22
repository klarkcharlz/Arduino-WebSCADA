"""наши представления"""
from flask import render_template, request

from web_form import TimeSelectForm  # наши формы
from logging_config import logger  # наше логирование
from server_func import (clear_cache, get_date, valid_time_period, select_db,
                         data_preparation, get_column_name)  # доп.функции


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
        # подготавливаем данные к отправки в шаблонизатор
        data, column = data_preparation(request, select_data)
        return render_template('arduino.html', data=data, column=column)

    data = get_column_name()  # имена столбцов из бд, для checkbox'сов
    return render_template('select.html', form=form, data=data)  # страница для получение данных от пользователя


def add_header(r):
    return clear_cache(r)


def test():
    """Работаем над календарем"""
    return render_template('test/test.html')

