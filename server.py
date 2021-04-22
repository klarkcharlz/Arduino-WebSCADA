from flask import Flask  # сервер


import views  # наши представления
from config import SECRET_KEY  # для csrf_token


app = Flask(__name__)  # обьект нашего сервера
app.config['SECRET_KEY'] = SECRET_KEY  # для csrf_token


@app.route('/', methods=('GET', 'POST'))
def select():
    """Главная страница"""
    return views.select()


@app.after_request
def add_header(r):
    """Боремся с кэшированием"""
    return views.add_header(r)


@app.route('/test/calender')
def test_calender():
    """Тестируем календари"""
    return views.test_calender()


@app.route('/test/trend')
def test_trend():
    """Тестируем тренды"""
    return views.test_trend()

