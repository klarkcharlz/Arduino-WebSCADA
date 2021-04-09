from flask import Flask, render_template, request
from datetime import datetime


from models import Monitoring
from web_form import TimeSelectForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'


@app.route('/Arduino/')
def main():
    data = Monitoring.select()
    return render_template('arduino.html', data=data)


@app.route('/', methods=('GET', 'POST'))
def select():
    form = TimeSelectForm()
    if request.method == 'POST' and form.validate_on_submit():  # Если метод запроса - POST и если поля формы валидны
        start = (request.form.get('start_time'))
        end = (request.form.get('end_time'))
        print(f"{start} - {end}")

        if datetime.strptime(start, '%Y-%m-%d %H:%M:%S') > datetime.now() or \
                datetime.strptime(end, '%Y-%m-%d %H:%M:%S') < datetime.strptime(start, '%Y-%m-%d %H:%M:%S'):
            return f"Некорректно задан диапазон"

        data = Monitoring.select().where(Monitoring.up_date >= start).where(Monitoring.up_date <= end)
        if not data:
            return "Извините но за данный временной промежуток отсутствуют данные"

        return render_template('arduino.html', data=data)

    return render_template('select.html', form=form)


if __name__ == "__main__":
    app.run()
