# whiterabbit/middleware.py

class MiddlewareManager:
    """
    Manages middleware functions.
    Middleware are functions that take (request, response=None) and can modify either.
    """
    def __init__(self):
        self.middlewares = []

    def add(self, func):
        """Register a middleware function."""
        if callable(func):
            self.middlewares.append(func)
        else:
            raise ValueError("Middleware must be a callable function")

    def execute_request(self, request):
        """Run middleware before route handler."""
        for middleware in self.middlewares:
            middleware(request)

    def execute_response(self, request, response):
        """Run middleware after route handler (optional response modifications)."""
        for middleware in self.middlewares:
            middleware(request, response)
        return response
