from x_app.view_model import XPageModel
from models.news import News


class LatestNewsViewModel(XPageModel):
    __template_name__ = 'index.html'

    def __init__(self):
        super().__init__('LatestNews')

    @property
    def news(self):
        return News.all()

