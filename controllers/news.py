from views.latest_news import LatestNewsViewModel
from x_app.controller import XController
from x_app.view_model import XPageModel


class NewsController(XController):
    def setup_endpoints(self):
        super().register_view_model('/', LatestNewsViewModel, 'latest')