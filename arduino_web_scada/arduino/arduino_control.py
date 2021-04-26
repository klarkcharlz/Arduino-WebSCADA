"""Получение, отправка данных и запись в бд"""
from asyncio import sleep  # асинхронность
from datetime import datetime  # для замеров скорости чтения
import time  # для задержки


# наши модули
from arduino_web_scada.web_server.models import Monitoring  # наши модели
from arduino_web_scada.utils.config import TOTAL_SENSOR, ACTUAL_SENSOR  # необходимые конфиги
from arduino_web_scada.utils.logging_config import logger  # логирование
from arduino_web_scada.utils.exchange_dat import shelve_read, load_ser, shelve_write


async def arduino_data_read():
    """Считывание данных от Arduino и их запись в бд"""
    ser = load_ser()  # получаем обькт соединения для работы
    print(ser)
    while True:  # проверяем соединение
        # в бесконечном цикле раз в 3 секунды опрашиваем датчики
        # проверяем флаг активности соединения
        if not shelve_read('flag'):  # если по нажатии кнопки стоп соединение было разорвано прекращаем опрос
            ser.close()
            logger.info(f'Закрываем соединение')  # фиксируем отключение
            time.sleep(3)  # немного подождем
            break
        data = {}  # для хранения принятых данных
        start_time = datetime.now()  # запоминаем текущее время для замеров
        ser.write(bytes('r', 'utf-8'))  # отправляем команду на считывание и передачу данных с датчиков
        for _ in range(TOTAL_SENSOR):  # считываем линии до символа '\n'
            # парсим и сохраняем
            serial_data = ser.readline().decode('utf-8').strip()
            serial_data = serial_data.split()
            data[serial_data[0]] = serial_data[1]

        # проверка принятых данных, фиксирование скорости замера
        shelve_write('last_data', data)  # сохранение последних данных
        logger.info(f'receive data:\n {data}.\nДанные получены за {datetime.now() - start_time} секунд.')
        data_for_insert_db = {}  # подготавливаем данные для записи в БД
        for sensor in ACTUAL_SENSOR:  # вытаскиваем из данных необходимые значения
            data_for_insert_db[sensor] = data.get(sensor, None)  # что то могло не прийти или прийти с  ошибкой

        monitoring = Monitoring(**data_for_insert_db)
        monitoring.save()  # производим запись в бд
        logger.info('data written to database')  # фиксируем запись

        # очищаем данные
        data_for_insert_db.clear()
        data.clear()

        # идем спать
        await sleep(3)
