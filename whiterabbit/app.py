from wsgiref.simple_server import make_server
import os
from .router import Router
from .response import Response

class App:
    def __init__(self):
        self.router = Router()
        # Templates and static inside src
        self.templates_folder = os.path.join(os.getcwd(), "src", "templates")
        self.static_folder = os.path.join(os.getcwd(), "src", "static")

    def route(self, path):
        def decorator(func):
            self.router.add_route(path, func)
            return func
        return decorator

    def render_template(self, template_name, context={}):
        template_path = os.path.join(self.templates_folder, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template {template_name} not found in {self.templates_folder}")
        with open(template_path) as f:
            content = f.read()
        for k, v in context.items():
            content = content.replace(f"{{{{ {k} }}}}", str(v))
        return content

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "/")
        # Serve static files
        if path.startswith("/static/"):
            file_path = os.path.join(self.static_folder, path[len("/static/"):])
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    data = f.read()
                start_response("200 OK", [("Content-Type", "text/css")])
                return [data]
            else:
                start_response("404 NOT FOUND", [("Content-Type", "text/plain")])
                return [b"Static file not found"]

        # Route handling
        class Request:
            def __init__(self, path):
                self.path = path

        request = Request(path)
        response = self.router.handle(request)
        start_response(response.status, response.headers)
        return [response.body.encode()]

    def run(self, host="127.0.0.1", port=8000):
        server = make_server(host, port, self)
        print(f"WhiteRabbit running on http://{host}:{port}")
        server.serve_forever()
