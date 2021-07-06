from flask_wtf import FlaskForm
from wtforms import *
from wtforms.fields.html5 import EmailField
from wtforms.validators import *


class LoginForm(FlaskForm):
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

    def get_user_data(self):
        return {'email': self.email.data,
                'password': self.password.data,
                'remember_me': self.remember_me.data}
