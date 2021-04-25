"""наши конфиги"""
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

# Arduino
ACTUAL_SENSOR = config['Arduino']['ACTUAL_SENSOR'].split(", ")  # актуальные датчики с которых пишим показания
TOTAL_SENSOR = len(ACTUAL_SENSOR)
SPEEDS = list(map(int, config['Arduino']['SPEEDS'].split(", ")))

# Server
SECRET_KEY = config['Server']['SECRET_KEY']   # для csrf_token токена

# Database
DATABASE_NAME = config['Database']['NAME']  # имя базы данныъ

# Браузер
WEBBROWSERS = config['Webbrowser']['WEBBROWSERS'].split(", ")
URL = config['Webbrowser']['URL']

if __name__ == "__main__":
    print(ACTUAL_SENSOR)
    print(TOTAL_SENSOR)
    print(SECRET_KEY)
    print(DATABASE_NAME)
    print(SPEEDS)
    print(WEBBROWSERS)
    print(URL)




