import requests

from .app import App


class ESI:
    URL_ESI = 'https://esi.evetech.net/latest'

    def __init__(self, client_id=None, scope=None, jwt_file_path=None):
        self.app = App(client_id, scope, jwt_file_path)

    def get(self, endpoint):
        access_token = self.app.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(self.URL_ESI + endpoint, headers=headers)
        return response.json()
