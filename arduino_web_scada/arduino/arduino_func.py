"""Вспомогательные функции для работы с ардуино"""
import serial  # для работы с портом
import serial.tools.list_ports  # список портов
import sys
import glob


def serial_ports():
    """Поиск доступных портов"""
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def find_arduino():
    """Автоопределение Arduino"""
    ports = serial.tools.list_ports.comports()
    commPort = 'None'
    numConnection = len(ports)
    for i in range(0, numConnection):
        port = ports[i]
        strPort = str(port.manufacturer)
        if 'Arduino' in strPort:
            commPort = port
            break
    return str(commPort).split(" - ")[0]


if __name__ == "__main__":
    print(serial_ports())
    print(find_arduino())
