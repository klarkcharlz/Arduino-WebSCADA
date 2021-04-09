from flask_wtf import FlaskForm
from wtforms import DateTimeField, SubmitField
from wtforms.validators import DataRequired


class TimeSelectForm(FlaskForm):
    start_time = DateTimeField(label='Начало',
                               validators=[DataRequired(message="Введите дату начала в соответствии с формой.")],
                               format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(label='Конец',
                             validators=[DataRequired(message="Введите дату конца в соответствии с формой.")],
                             format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField(label='Отправить')
