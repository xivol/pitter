
class RouteParam:
    def __init__(self, type, route_name, model_name=None):
        self.type = type
        self.name = route_name
        if model_name:
            self.model = model_name
        else:
            self.model = route_name

    def __str__(self):
        return f'<{self.type}:{self.name}>'

    def __repr__(self):
        return str(self)