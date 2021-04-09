from peewee import SqliteDatabase, Model, DateTimeField, FloatField


db = SqliteDatabase('arduino_monitoring.db')


class Monitoring(Model):
    DS18B20_t = FloatField(null=True)
    DHT11_h = FloatField(null=True)
    DHT11_t = FloatField(null=True)
    illumination = FloatField(null=True)
    up_date = DateTimeField()

    class Meta:
        database = db
