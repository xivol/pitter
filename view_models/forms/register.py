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
        if self.field.class_.query(self.field == value).first():
            raise ValidationError(f"{self.field.key.capitalize()} must be unique.")


class UniqueText(Unique):
    def __init__(self, field, case_sensitive=False):
        super().__init__(field)
        self.case_sensitive = case_sensitive

    def __call__(self, form, field):
        if not self.case_sensitive:
            field.data = field.data.lower()
        super().__call__(form, field)


class RegisterForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(),
        Length(min=3, max=25),
        Regexp('^\w+$', message='Only letters, numbers or underscore are allowed in username.'),
        UniqueText(User.username)
    ])
    email = EmailField('Email', [
        DataRequired(),
        Length(min=5, max=35),
        Email(),
        UniqueText(User.email)
    ])
    password = PasswordField('Password', [
        DataRequired(),
        EqualTo('password_confirm', message='Passwords don\'t match')
    ])
    password_confirm = PasswordField('Repeat Password', [
        DataRequired()
    ])

    first_name = StringField('Firstname', [
        Length(min=2, max=25)
    ])
    last_name = StringField('Lastname', [
        Optional(),
        Length(min=2, max=25)
    ])
    about = TextAreaField("Write about yourself", [
        Optional(),
        Length(min=2, max=256)
    ])

    submit = SubmitField('Sign Up')

    def get_user_data(self):
        return {'username': self.username.data.lower(),
                'email': self.email.data.lower(),
                'password': self.password.data,
                'first_name': self.first_name.data,
                'last_name': self.last_name.data,
                'about': self.about.data}
