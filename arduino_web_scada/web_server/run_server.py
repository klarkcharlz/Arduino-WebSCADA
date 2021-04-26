"""Запуск сервера"""
from multiprocessing import Process  # для управления сервером


from arduino_web_scada.web_server.server import app  # наш сервер


server = None  # наш будущий сервер для управления из графического приложения


def start_server():
    """Запуск сервера"""
    global server
    server = Process(target=app.run)
    server.start()


def stop_server():
    """Остановка сервера"""
    global server
    server.terminate()


if __name__ == "__main__":
    app.run()
