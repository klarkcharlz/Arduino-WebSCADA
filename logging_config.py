"""Настройка логгирования"""
from loguru import logger

logger.add('./log/database.log', format='{time} {level} {message}', level='DEBUG')
