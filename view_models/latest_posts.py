from x_app.view_model import XPageModel
from models.posts import Posts


class LatestNewsViewModel(XPageModel):
    __template_name__ = 'layout.html'

    def __init__(self):
        super().__init__('Latest')

    @property
    def news(self):
        return Posts.all()

