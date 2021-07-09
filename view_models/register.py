from flask import current_app, url_for, flash
from werkzeug.utils import redirect

from view_models.forms.register import RegisterForm
from x_app.navigation import XNav, XNavigationMixin
from x_app.view_model import XFormPage


class RegisterViewModel(XFormPage, XNavigationMixin):
    __template_name__ = 'register.html'

    def __init__(self):
        super().__init__("Sign Up")

    def make_form(self):
        return RegisterForm()

    def on_form_success(self, form):
        try:
            data = form.get_user_data()
            current_app.identity_provider.register(**data)
            current_app.identity_provider.try_login(**data)
            return redirect(f'/user/{form.username.data}')
        except Exception as err:
            flash(err.args,'danger')
            return self.on_form_error(form)


    def on_form_error(self, form):
        return self.render_template()

    @property
    def navigation(self):
        return [XNav('Sign In', url_for('auth.login'), 'btn-light')]


