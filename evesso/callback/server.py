"""This module implements a subclassed TCPServer.
The server listens for a single GET request and then shuts down.
The server then returns the path that was requested.
This path is then parsed and the query string parameters are extracted."""
import http.server
import pathlib
import socketserver


class Server(socketserver.TCPServer):
    """Subclassed TCPServer to enable extraction of requested call path"""

    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        self.path = None
        super().__init__(*args, **kwargs)

    def set_path(self, path: str) -> None:
        """Store the requested path on the server instance for later retrieval
        :param path: str the URL path that was request byt he auth server
        :return: None
        """

        self.path = path


class Handler(http.server.BaseHTTPRequestHandler):
    """Handler to append the requested call path to the server.
    Returns a simple generic json response."""

    def _set_response(self) -> None:
        """Set the response that will be sent to the request sender"""

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self) -> None:
        """Respond to a GET request.
        Store the requested path on the server instance.
        Send a simple HTML page indicating the user can
        close the window
        """

        self.server.set_path(self.path)
        self.send_response(200, "OK")
        self.end_headers()

        index = pathlib.Path(__file__).resolve().parent / 'index.html'

        with open(index, 'rb') as file:
            response = file.read()
            self.wfile.write(response)


def listen_for_callback() -> str:
    """Run the server on port 80 (default http) and listen for a single request.
    The handler will append the called path to the server object's `path` attribute.
    This function will then return the path string stored on the server.
    :return: str the path that was called
    """

    with Server(("", 80), Handler) as httpd:
        while httpd.path is None:
            httpd.handle_request()
        return httpd.path
