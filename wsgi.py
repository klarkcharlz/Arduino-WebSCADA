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

        select_data = Monitoring.select().where(Monitoring.up_date >= start).where(Monitoring.up_date <= end)
        if not select_data:
            return "Извините но за данный временной промежуток отсутствуют данные"

        column = []
        data = []
        DS18B20_t = (request.form.get('DS18B20_t'))
        if DS18B20_t:
            column.append('DS18B20_t')
        DHT11_h = (request.form.get('DHT11_h'))
        if DHT11_h:
            column.append('DHT11_h')
        DHT11_t = (request.form.get('DHT11_t'))
        if DHT11_t:
            column.append('DHT11_t')
        illumination = (request.form.get('illumination'))
        if illumination:
            column.append('illumination')

        for row in select_data:
            temp = {}
            for col in column:
                temp[col] = row.__dict__['__data__'][col]
                temp['up_date'] = row.__dict__['__data__']['up_date']
            data.append(temp)

        # print(column)
        # print(DS18B20_t, DHT11_h, DHT11_t, illumination)

        return render_template('arduino.html', data=data, column=column)

    data = list(Monitoring.select()[0].__dict__['__data__'].keys())[1:-1]
    # print(data)
    return render_template('select.html', form=form, data=data)


@app.after_request
def add_header(r):
    """что бы избавиться от кеширования"""
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.run()
