import serial
from asyncio import sleep, get_event_loop, gather
from datetime import datetime


import models


ser = serial.Serial('/dev/ttyACM0')
models.Monitoring.create_table()
data = {}


async def arduino_data_read():
    while True:
        try:
            receive_data = ser.readline().decode('utf-8').strip()
        except Exception as err:
            print(err)
            print(receive_data)
            print("Error data!")
        else:
            if receive_data == 'END':
                if len(data) == 4:
                    print(data)
                    monitoring = models.Monitoring(DS18B20_t=data.get('Dallas-DS18B20(t°C)', None),
                                                   DHT11_h=data.get('DHT11(h%)', None),
                                                   DHT11_t=data.get('DHT11(t°C)', None),
                                                   illumination=data.get('illumination', None),
                                                   up_date=datetime.now())
                    monitoring.save()
                    data.clear()
                else:
                    pass
            else:
                try:
                    receive_data = receive_data.split()
                    try:
                        val = float(receive_data[1])
                    except Exception as err:
                        print(err)
                        val = None
                    data[receive_data[0][:-1]] = val
                except Exception as err:
                    print(err)
                    print("Data not valid format. valid date form if 'name: float(value)'!")
    await sleep(10)


async def work_with_async():
    await gather(arduino_data_read())


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(work_with_async())
    ser.close()
