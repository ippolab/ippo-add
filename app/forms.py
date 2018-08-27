# -*- coding: utf-8 -*-

import phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, Length

from app import app


class RegistrationForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    surname = StringField('Ваша фамилия', validators=[DataRequired()])
    lastname = StringField('Ваше отчество', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(),
                                              Email(message="Неправильный формат. Пример: john.smith@example.com.")])
    phone = StringField('Телефон', validators=[DataRequired(),
                                               Length(min=10,
                                                      max=19,
                                                      message="Слишком короткая строка для телефонного номера")])
    group = SelectField('Группа', validators=[DataRequired()],
                        choices=list(zip(app.config['GROUPS'], app.config['GROUPS'])))
    department = SelectField('Кафедра', validators=[DataRequired()],
                             choices=list(zip(app.config['DEPARTMENTS'], app.config['DEPARTMENTS'])))
    data_processing = BooleanField('Я согласен на обработку данных', validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def validate_phone(self, phone):
        if not 9 < len(phone.data) < 20:
            return

        try:
            input_number = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError('Неправильный телефонный номер')
        except phonenumbers.NumberParseException:
            raise ValidationError('Неправильный формат номера')
