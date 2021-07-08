from werkzeug.exceptions import abort

from view_models.forms.post import NewTextPostForm
from view_models.mixins.navigation import NavigationViewModel
from controllers.params.user import USER_PARAM, get_user
from x_app.view_model import XPageModel

from models.posts import Post


class UserFeedViewModel(XPageModel, NavigationViewModel):
    __request_params__ = {USER_PARAM.name}
    __template_name__ = 'timeline.html'

    def __init__(self, **url_providers):
        super().__init__('User')
        self.user = None
        self.urls = url_providers

    def on_request(self, request):
        self.user = None
        return get_user(self, self.on_user_found,
                 on_user_not_found=lambda: abort(404),
                 on_param_error=lambda: abort(400))

    def on_user_found(self, user):
        self.user = user
        return super().render_template()

    @property
    def feed(self):
        # TODO: filter public
        if self.user is not None:
            return self.user.posts
        else:
            return Post.all()

    @property
    def new_post_form(self):
        form = NewTextPostForm()
        if self.user.is_authenticated:
            form.author_id.data = self.user.id
        return form
