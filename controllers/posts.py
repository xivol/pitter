from view_models.timeline import IndexViewModel
from x_app.controller import XController


class PostsController(XController):
    def setup_endpoints(self):
        super().register_view_model('/', IndexViewModel, 'latest')