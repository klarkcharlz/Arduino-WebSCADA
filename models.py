"""Наши модели"""
from peewee import SqliteDatabase, Model, DateTimeField, FloatField, datetime  # всё что нужно
from datetime import datetime  # для поля up_date


import config


db = SqliteDatabase(config.DATABASE_NAME)  # подключение к бд


class Monitoring(Model):
    """Модель наших данных"""
    DS18B20_t = FloatField(null=True)
    DHT11_h = FloatField(null=True)
    DHT11_t = FloatField(null=True)
    illumination = FloatField(null=True)
    up_date = DateTimeField(default=datetime.now())

    class Meta:
        database = db
