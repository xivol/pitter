from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import *

from models.users import User


class Unique:
    def __init__(self, entity, field):
        self.entity = entity
        self.field = field

    def __call__(self, form, field):
        value = field.data
        if self.entity.query(self.entity.__getattr__[self.field] == value).first():
            raise ValidationError("Пользовательс таким email уже есть")


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', [
        Length(min=4, max=25),
        Unique(User, 'name')
    ])
    email = EmailField('Почта', [
        Length(min=6, max=35),
        Unique(User, 'email')
    ])

    password = PasswordField('Пароль', [
        DataRequired(),
        EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Повторите пароль', [DataRequired()])

    about = TextAreaField("Немного о себе", [
        Optional(),
        Length(min=2, max=256)
    ])
    submit = SubmitField('Войти')
