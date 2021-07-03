class XNav:
    def __init__(self, title, url, style=None):
        self.title = title
        self.url = url
        self.style = style if style is not None else ""


class XNavigationMixin:
    @property
    def navigation(self):
        return []