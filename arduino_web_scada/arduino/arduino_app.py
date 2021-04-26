"""Главное приложение"""
from asyncio import get_event_loop, gather  # для асинхронного выполнения задач


# наши модули
from arduino_web_scada.arduino.tk_gui import gui
from arduino_web_scada.utils.logging_config import logger


async def work_with_async():  # наши асинхронные задачи
    """здесь будем запускать на выполнение наши асинхронные функции"""
    await gather(gui())  # передаем очередь на выполнение


def run():
    try:
        loop = get_event_loop()  # создаем цикл обработчик асинхронных задач и запускаем его
        loop.run_until_complete(work_with_async())
    except Exception as err:  # пока отлавливаем и смотрим какие могут быть ошибки в течении работы скрипта
        logger.error(f'{type(err)} : {err}')


if __name__ == "__main__":
    run()
