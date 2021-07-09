from flask import url_for, current_app

from view_models.user_feed import UserFeedViewModel
from x_app.navigation import XNavigationMixin, XNav
from x_app.view_model import XPageModel
from models.posts import Post


class IndexViewModel(UserFeedViewModel):

    def __init__(self, **url_providers):
        super().__init__('Latest', **url_providers)
        self.user = current_app.identity_provider.current_user

    @property
    def feed(self):
        # TODO: filter public
        return sorted(Post.all(), key=lambda p: p.created_date, reverse=True)

    def on_request(self, request):
        return super().render_template()
