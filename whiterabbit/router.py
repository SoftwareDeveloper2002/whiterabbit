from .response import Response

class Router:
    def __init__(self):
        self.routes = {}

    # Add this method to explicitly add routes
    def add_route(self, path, func):
        self.routes[path] = func

    def route(self, path):
        def decorator(func):
            self.add_route(path, func)  # now it exists
            return func
        return decorator

    def handle(self, request):
        path = request.path.rstrip("/") or "/"
        func = self.routes.get(path)
        if func:
            result = func(request)
            if isinstance(result, str):
                return Response(result, status="200 OK")
            return result
        return Response("404 Not Found", status="404 NOT FOUND")
