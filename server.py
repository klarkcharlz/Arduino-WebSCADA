from flask import Flask


import config
import views


app = Flask(__name__)  # обьект нашего сервера
app.config['SECRET_KEY'] = config.SECRET_KEY


@app.route('/', methods=('GET', 'POST'))
def select():
    return views.select()


@app.after_request
def add_header(r):
    return views.add_header(r)


@app.route('/test/')
def test():
    return views.test()
