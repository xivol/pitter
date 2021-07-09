from flask import current_app, Response, request
from werkzeug.exceptions import default_exceptions

from view_models.error import ErrorViewModel
from x_app.controller import XController


class ErrorController(XController):
    def setup_endpoints(self):
        pass

    def register_in_app(self, application, **config):
        super().register_in_app(application, **config)
        for code in default_exceptions:
            application.register_error_handler(code, self._handle_http_exception)

    def _handle_http_exception(self, e):
        if e.code < 400:
            return Response.force_type(e, request.environ)
        elif e.code == 404:
            evm = ErrorViewModel(e.code, "The page you're looking for was not found", "Page Not Found")
            return evm.render_template(), 404
        elif 400 <= e.code < 500:
            evm = ErrorViewModel(e.code, e.description)
            return evm.render_template(), e.code
        else:
            evm = ErrorViewModel(e.code, "Something went wrong")
            return evm.render_template(), 500
