from flask import url_for, current_app

from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XPageModel
from models.posts import Post


class TimelineViewModel(XPageModel, XNavigationMixin):
    @property
    def feed(self):
        # TODO: filter public
        return Post.all()

    @property
    def user(self):
        return current_app.identity_provider.current_user

    @property
    def navigation(self):
        if not current_app.identity_provider.current_user.is_authenticated:
            return [XNav('Sign In', url_for('auth.login'), 'btn-outline-secondary'),
                    XNav('Sign Up', url_for('auth.register'), 'btn-outline-primary')]
        else:
            return [XNav('Sign Out', url_for('auth.logout'), 'btn-outline-secondary')]


class IndexViewModel(TimelineViewModel):
    __template_name__ = 'timeline.html'

    def __init__(self):
        super().__init__('Latest')
