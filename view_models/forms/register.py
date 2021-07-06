from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import *

from models.users import User


class Unique:
    def __init__(self, field):
        self.field = field

    def __call__(self, form, field):
        value = field.data
        if self.field.class_.query(field == value).first():
            raise ValidationError(f"{self.field} must be unique")


class RegisterForm(FlaskForm):
    first_name = StringField('Firstname', [
        Length(min=2, max=25)
    ])
    last_name = StringField('Lastname', [
        Length(min=2, max=25)
    ])
    username = StringField('Username', [
        Length(min=4, max=25),
        Unique(User.username)
    ])
    email = EmailField('Email', [
        Length(min=6, max=35),
        Unique(User.email)
    ])

    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password', [DataRequired()])

    about = TextAreaField("Write about yourself", [
        Optional(),
        Length(min=2, max=256)
    ])
    submit = SubmitField('Sign Up')

    def get_user_data(self):
        return {'username': self.username.data,
                'email': self.email.data,
                'password': self.password.data,
                'first_name': self.first_name.data,
                'last_name': self.last_name.data,
                'about': self.about.data}
