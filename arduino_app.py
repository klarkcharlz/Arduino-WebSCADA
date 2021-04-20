from asyncio import get_event_loop, gather  # для асинхронного выполнения задач


# наши модули
from tk_gui import gui
from logging_config import logger


async def work_with_async():  # наши асинхронные задачи
    """здесь будем запускать на выполнение наши асинхронные функции"""
    await gather(gui())  # передаем очередь на выполнение


if __name__ == "__main__":
    try:
        loop = get_event_loop()  # создаем цикл обработчик асинхронных задач и запускаем его
        loop.run_until_complete(work_with_async())
    except Exception as err:  # пока отлавливаем и смотрим какие могут быть ошибки в течении работы скрипта
        logger.error(f'{type(err)} : {err}')
