import serial  # для работы с портом
from asyncio import sleep, get_event_loop, gather  # асинхронность
import time  # для задержки

# наши модули
import models
import config
from logging_config import logger


async def arduino_data_read():
    """Считывание данных от Arduino и их запись в бд"""
    while True:
        data = {}
        ser.write(bytes('r', 'utf-8'))  # отправляем команду на считывание и передачу данных с датчиков
        for _ in range(config.TOTAL_SENSOR):  # считываем линии до символа '\n'
            serial_data = ser.readline().decode('utf-8').strip()
            serial_data = serial_data.split()
            data[serial_data[0]] = serial_data[1]

        logger.info(f'receive data: {data}')  # проверка принятых данных

        data_for_insert_db = {}
        for sensor in config.ACTUAL_SENSOR:  # вытаскиваем из данных необходимые значения
            data_for_insert_db[sensor] = data.get(sensor, None)  # что то могло не прийти или прийти с  ошибкой

        monitoring = models.Monitoring(**data_for_insert_db)
        monitoring.save()  # производим запись в бд
        logger.info('data written to database')

        # очищаем данные
        data_for_insert_db.clear()
        data.clear()

        # идем спать
        await sleep(3)


async def work_with_async():
    """здесь будем запускать на выполнение наши асинхронные функции"""
    await gather(arduino_data_read())


if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)  # создаем соединение
        time.sleep(3)  # немного подождем
        loop = get_event_loop()  # создаем цикл обработчик асинхронных задач и запускаем его
        loop.run_until_complete(work_with_async())
    except Exception as err:  # пока отлавливаем и смотрим какие могут быть ошибки в течении работы скрипта
        logger.error(f'{type(err)} : {err}')
    finally:
        ser.close()  # в случае чего закрываем соединение

