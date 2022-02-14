"""This module implements a subclassed TCPServer.
The server listens for a single GET request and then shuts down.
The server then returns the path that was requested.
This path is then parsed and the query string parameters are extracted."""
import http.server
import json
import socketserver
import urllib


class Server(socketserver.TCPServer):
    """Subclassed TCPServer to enable extraction of requested call path"""

    def __init__(self, *args, **kwargs):
        self.allow_reuse_address = True
        self.path = None
        super().__init__(*args, **kwargs)

    def set_path(self, path) -> None:
        self.path = path


class Handler(http.server.BaseHTTPRequestHandler):
    """Handler to append the requested call path to the server.
    Returns a simple generic json response."""

    def _set_response(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self) -> None:
        self.server.set_path(self.path)
        self.send_response(200, "OK")
        self.end_headers()

        # TODO: display webpage saying to close window
        data = {
            'status': 200,
            'message': 'You may close this page.'
        }
        response = json.dumps(data).encode("utf-8")
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


def get_callback_data() -> dict:
    """Run the server to listen for a callback request.
    Extract the requested url path and parwse it.
    Return the parsed query string as a dict with the
    structure of `{str: list}`.

    Example output:
        {'code': ['abdcefghijklmnopqrstuvwxyz0123456789'], 'state': ['secret']}

    :return: dict query string parameters from the callback
    """

    path = listen_for_callback()
    parsed_path = urllib.parse.urlparse(path)
    return urllib.parse.parse_qs(parsed_path.query)
