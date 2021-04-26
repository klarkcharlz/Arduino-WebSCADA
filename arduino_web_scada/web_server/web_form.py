"""Фласк формы"""
from flask_wtf import FlaskForm  # класс формы
from wtforms import DateTimeField, SubmitField, SelectField  # типы полей
from wtforms.validators import DataRequired  # валидация


class TimeSelectForm(FlaskForm):
    """Форма для получения временного промежутка"""
    start_time = DateTimeField(label='Начало',
                               validators=[DataRequired(message="Введите дату начала в соответствии с формой.")],
                               format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(label='Конец',
                             validators=[DataRequired(message="Введите дату конца в соответствии с формой.")],
                             format='%Y-%m-%d %H:%M:%S')
    vizual_type = SelectField(choices=[('table', 'Таблица'), ('trend', 'Тренд')])
    submit = SubmitField(label='Отправить')
