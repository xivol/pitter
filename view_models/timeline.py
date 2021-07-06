from flask import url_for
from flask_login import current_user

from view_models.forms.post import NewTextPostForm
from x_app.identity_provider import XIdentityMixin
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XPageModel
from models.posts import Post


class TimelineViewModel(XPageModel, XIdentityMixin, XNavigationMixin):
    @property
    def posts(self):
        # TODO: filter public
        return Post.all()

    @property
    def form(self):
        frm = NewTextPostForm()
        if self.user.is_authenticated:
            frm.author_id.data = self.user.id
        return frm

    @property
    def navigation(self):
        if not current_user.is_authenticated:
            return [XNav('Sign In', url_for('auth.login'), 'btn-outline-secondary'),
                    XNav('Sign Up', url_for('auth.register'), 'btn-outline-primary')]
        else:
            return [XNav('Sign Out', url_for('auth.logout'), 'btn-outline-secondary')]


class IndexViewModel(TimelineViewModel):
    __template_name__ = 'timeline.html'

    def __init__(self):
        super().__init__('Latest')
