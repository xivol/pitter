from flask import current_app, url_for, abort
from werkzeug.utils import redirect

from view_models.forms.post import NewTextPostForm
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XPageModel

from models.posts import Post
from models.users import User

USERNAME_PARAM = 'username'


class UserFeedViewModel(XPageModel, XNavigationMixin):
    __request_params__ = {USERNAME_PARAM}
    __template_name__ = 'timeline.html'

    def __init__(self):
        super().__init__('User')
        self.user = None

    def dispatch_request(self, *args, **kwargs):
        super().parse_params(kwargs)
        self.user = None
        if self.username:
            u = User.query(User.username == self.username).first()
            if u is not None:
                self.user = u
                return super().render_template()
            else:
                return abort(404)
        else:
            return redirect(url_for('latest'))

    @property
    def feed(self):
        # TODO: filter public
        if self.user is not None:
            return self.user.posts
        else:
            return Post.all()

    @property
    def new_post_form(self):
        frm = NewTextPostForm()
        if self.user.is_authenticated:
            frm.author_id.data = self.user.id
        return frm

    @property
    def navigation(self):
        print(current_app.identity_provider.current_user)
        if not current_app.identity_provider.current_user.is_authenticated:
            return [XNav('Sign In', url_for('auth.login'), 'btn-outline-secondary'),
                    XNav('Sign Up', url_for('auth.register'), 'btn-outline-primary')]
        else:
            return [XNav('Sign Out', url_for('auth.logout'), 'btn-outline-secondary')]
