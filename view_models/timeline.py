from flask import url_for
from flask_login import current_user

from x_app.identity_provider import XIdentityMixin
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XPageModel
from models.posts import Posts


class TimelineViewModel(XPageModel, XIdentityMixin, XNavigationMixin):
    @property
    def posts(self):
        # TODO: filter public
        return Posts.all()

    @property
    def navigation(self):
        if not current_user.is_authenticated:
            return [XNav('Sign In', url_for('user.login'), 'btn-outline-secondary'),
                    XNav('Sign Up', url_for('user.register'), 'btn-outline-primary')]
        else:
            return [XNav('Sign Out', url_for('user.logout'), 'btn-outline-secondary')]


class IndexViewModel(TimelineViewModel):
    __template_name__ = 'index.html'

    def __init__(self):
        super().__init__('Latest')


