import requests

from .const import HEADERS, TOKEN_URL


def get_refresh_jwt(client_id: str, scope: str, refresh_token: str) -> dict:
    """Retrieve stored refresh token and send it in request to get updated access token

    :param client_id: str Client ID associated with your application, found at https://developers.eveonline.com/applications
    :param scope: str a space-delimited string of scopes, found at https://developers.eveonline.com/applications
    :param refresh_token: str stored refresh_token from authorization request or previous refresh request
    :return: dict JWT received from authorization server containing access token and refresh token
    """

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'scope': scope
    }
    response = requests.post(TOKEN_URL, data=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()
