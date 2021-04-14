import serial
from asyncio import sleep, get_event_loop, gather
from datetime import datetime
import time


import models


async def arduino_data_read():
    while True:
        ser.write(bytes('r', 'utf-8'))
        for _ in range(4):  # считываем 4 линии до символа '\n'
            serial_data = ser.readline().decode('utf-8').strip()
            serial_data = serial_data.split(": ")
            data[serial_data[0]] = serial_data[1]
        print(data)
        monitoring = models.Monitoring(DS18B20_t=data.get('Dallas-DS18B20(t°C)', None),
                                       DHT11_h=data.get('DHT11(h%)', None),
                                       DHT11_t=data.get('DHT11(t°C)', None),
                                       illumination=data.get('illumination', None),
                                       up_date=datetime.now())
        monitoring.save()
        data.clear()
        await sleep(3)


async def work_with_async():
    await gather(arduino_data_read())


if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1)
        data = {}
        time.sleep(3)
        loop = get_event_loop()
        loop.run_until_complete(work_with_async())
    except Exception as err:
        print(type(err))
        print(err)
    finally:
        ser.close()

