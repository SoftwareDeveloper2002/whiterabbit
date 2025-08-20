from wsgiref.simple_server import make_server
import os
from .router import Router
from .response import Response
from .middleware import MiddlewareManager

class App:
    def __init__(self):
        self.router = Router()
        # Templates and static inside src
        self.templates_folder = os.path.join(os.getcwd(), "src", "templates")
        self.static_folder = os.path.join(os.getcwd(), "src", "static")
        # Middleware manager
        self.middlewares = MiddlewareManager()

    # Route decorator
    def route(self, path):
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    # Template rendering
    def render_template(self, template_name, context={}):
        template_path = os.path.join(self.templates_folder, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template {template_name} not found in {self.templates_folder}")
        with open(template_path) as f:
            content = f.read()
        for k, v in context.items():
            content = content.replace(f"{{{{ {k} }}}}", str(v))
        return content

    # Register middleware
    def add_middleware(self, func):
        self.middlewares.add(func)

    # WSGI callable
    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")

        # Serve static files
        if path.startswith("/static/"):
            file_path = os.path.join(self.static_folder, path[len("/static/"):])
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    data = f.read()
                start_response("200 OK", [("Content-Type", self.get_mime_type(file_path))])
                return [data]
            else:
                start_response("404 NOT FOUND", [("Content-Type", "text/plain")])
                return [b"Static file not found"]

        # Request object
        class Request:
            def __init__(self, path, environ):
                self.path = path
                self.environ = environ
                self.user_authenticated = False  # placeholder, can be used in middleware
                self.params = {}

        request = Request(path, environ)

        # Execute pre-route middleware
        self.middlewares.execute_request(request)

        # Route handling
        response = self.router.handle(request)

        # Execute post-route middleware
        response_body = self.middlewares.execute_response(request, response)

        start_response(response.status, response.headers)
        return [response_body.encode()]

    def get_mime_type(self, file_path):
        """Basic MIME types for static files"""
        if file_path.endswith(".css"):
            return "text/css"
        elif file_path.endswith(".js"):
            return "application/javascript"
        elif file_path.endswith(".png"):
            return "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            return "image/jpeg"
        elif file_path.endswith(".html"):
            return "text/html"
        else:
            return "application/octet-stream"

    def run(self, host="127.0.0.1", port=8000):
        server = make_server(host, port, self)
        print(f"WhiteRabbit running on http://{host}:{port}")
        server.serve_forever()
