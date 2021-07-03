from x_app.identity_provider import XIdentityMixin
from x_app.view_model import XPageModel
from models.posts import Posts


class TimelineViewModel(XPageModel, XIdentityMixin):
    @property
    def posts(self):
        # TODO: filter public
        return Posts.all()


class IndexViewModel(TimelineViewModel):
    __template_name__ = 'index.html'

    def __init__(self):
        super().__init__('Latest')


