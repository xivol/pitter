from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import *




class LoginForm(FlaskForm):
    email = EmailField('Почта', [DataRequired()])
    password = PasswordField('Пароль', [DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')