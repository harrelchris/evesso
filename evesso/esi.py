import os
import json
import time

import requests


class ESI:
    # URL_DEVELOPERS = "https://developers.eveonline.com/"
    # URL_UI = "https://esi.evetech.net/ui/"
    # URL_AUTHORIZE = "https://login.eveonline.com/v2/oauth/authorize/"
    URL_TOKEN = "https://login.eveonline.com/v2/oauth/token"
    URL_LATEST = "https://esi.evetech.net/latest"
    DATASOURCE = "tranquility"
    LANGUAGE = "en"

    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "accept": "application/json",
        "Accept-Language": "en",
        "Cache-Control": "no-cache"
        # "Host": "login.eveonline.com",  # Causes public endpoints to fail
    }

    def __init__(self, client_id=None, callback_url=None, scope=None):
        self.CLIENT_ID = client_id or os.environ.get('CLIENT_ID')
        if not self.CLIENT_ID:
            raise ValueError('Neither client_id parameter nor CLIENT_ID environment variable found.')

        self.CALLBACK_URL = callback_url or os.environ.get('CALLBACK_URL')
        if not self.CALLBACK_URL:
            raise ValueError('Neither callback_url parameter nor CALLBACK_URL environment variable found.')

        self.SCOPE = scope or os.environ.get('SCOPE')
        if not self.SCOPE:
            raise ValueError('Neither scope parameter nor SCOPE environment variable found.')

        self.jwt_file_path = "./jwt.json"

    def _build_endpoint_url(self, endpoint):
        # TODO: validate endpoint string
        return f'{self.URL_LATEST}{endpoint}?datasource={self.DATASOURCE}&language={self.LANGUAGE}'

    def _get_json_file_path(self):
        return './jwt.json'

    def _get_access_token(self):
        jwt = self._read_jwt_from_file()
        access_token = jwt.get('access_token')
        if access_token:

            return access_token

        jwt = self._refresh_access_token()
        access_token = jwt.get('access_token')
        if access_token:
            return access_token

        jwt = self._get_auth_token()
        access_token = jwt.get('access_token')
        if access_token:
            return access_token

    def _read_jwt_from_file(self):
        jwt = None
        try:
            file = open(self.jwt_file_path, 'r')
        except FileNotFoundError:
            file = open(self.jwt_file_path, 'w')
            json.dump({}, file)
        else:
            jwt = json.load(file)
        finally:
            file.close()
        return jwt

    def _refresh_access_token(self):
        # TODO: get new token
        # TODO: store it
        # TODO: return it
        print("refreshing token")

    def _get_auth_token(self):
        # TODO: get new token
        # TODO: store it
        # TODO: return it
        print("getting auth token")

    def get(self, endpoint: str) -> dict:
        """Make a request to an ESI endpoint.
        All parameterized endpoints should be complete with appropriate values.

        :param endpoint: str the endpoint to request
        :return: dict the json response from the endpoint
        """

        access_token = self._get_access_token()
        self.HEADERS.update(Authorization=f"Bearer {access_token}")
        url = self._build_endpoint_url(endpoint)
        # response = requests.get(url, headers=self.HEADERS)
        # response.raise_for_status()
        # return response.json()
        return {}


    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
