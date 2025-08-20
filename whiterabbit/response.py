# whiterabbit/response.py

class Response:
    def __init__(self, body, status="200 OK", headers=None):
        """
        Represents an HTTP response.

        :param body: The content to return (string)
        :param status: HTTP status, e.g., "200 OK"
        :param headers: List of tuples for HTTP headers, e.g., [("Content-Type", "text/html")]
        """
        self.body = body
        self.status = status
        self.headers = headers if headers else [("Content-Type", "text/html")]
