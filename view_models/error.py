from flask import url_for, current_app

from view_models.mixins.navigation import NavigationViewModel
from x_app.view_model import XPageModel


class ErrorViewModel(XPageModel, NavigationViewModel):
    __template_name__ = 'error.html'

    def __init__(self, code, description, title='Error'):
        super().__init__(title)
        self.code = code
        self.description = description
