"""Настройка логгирования"""
from loguru import logger

logger.add('log/arduinoWebScada.log', format='{time} {level} {message}', level='DEBUG')
