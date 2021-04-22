"""вспомогательные функции для веб-сервера"""
from logging_config import logger  # логирование
from datetime import datetime  # для проверки даты


from models import Monitoring  # Наши модели
from config import ACTUAL_SENSOR  # нужные конфиги


def clear_cache(r):
    """что бы избавиться от кеширования"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def get_date(request):
    """Получение даты из веб-формы"""
    start, end = request.form.get('start_time'), request.form.get('end_time')
    logger.info(f"Запрошен следующий временной промежуток: Начало: {start} - Конец: {end}")
    return start, end


def valid_time_period(start, end):
    """Проверка временного диапазона"""
    if datetime.strptime(start, '%Y-%m-%d %H:%M:%S') > datetime.now() or \
            datetime.strptime(end, '%Y-%m-%d %H:%M:%S') < datetime.strptime(start, '%Y-%m-%d %H:%M:%S'):
        logger.error(f"Некорректно задан диапазон")
        return False
    return True


def select_db(start, end):
    """Запрос в бд по заданному временному диапазону"""
    return Monitoring.select().where(Monitoring.up_date >= start).where(Monitoring.up_date <= end)


def data_preparation_for_table(request, select_data):
    """Подготовка данных для визуализации в виде таблицы"""
    column = []  # столбцы
    data = []  # данные для заполнения столбцов
    # смотрим какие данные нас интересуют и фиксируем это
    for sensor in ACTUAL_SENSOR:
        get_sensor = request.form.get(sensor)
        if get_sensor:
            column.append(sensor)
    logger.info(f'Запрошены данные по следующим показаниям: {column}')
    # подготовка необходимых данных
    for row in select_data:
        temp = [row.__dict__['__data__']['up_date']]
        for col in column:
            temp.append(row.__dict__['__data__'][col])
        data.append(temp)
    return data, column


def get_column_name():
    """Получение имен столбцов из бд, нас интересует получить список всех доступных показания"""
    data = list(Monitoring.select()[0].__dict__['__data__'].keys())[1:-1]  # имена столбцов из бд, для checkbox'сов
    logger.info(f'В БД находятся следующие данные: {data}(запрос для главной страницы)')
    return data
