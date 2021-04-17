"""Наши модели"""
from peewee import SqliteDatabase, Model, DateTimeField, FloatField  # всё что нужно


db = SqliteDatabase('arduino_monitoring.db')  # подключение к бд


class Monitoring(Model):
    """Модель наших данных"""
    DS18B20_t = FloatField(null=True)
    DHT11_h = FloatField(null=True)
    DHT11_t = FloatField(null=True)
    illumination = FloatField(null=True)
    up_date = DateTimeField()

    class Meta:
        database = db
