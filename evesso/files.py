import json
import time


def load_jwt(path: str) -> dict:
    """Open the file at `path` and read the stored JWT.

    :param path: str file path to the jwt.json file
    :return: dict the JWT containing an access token and refresh token
    """

    file = open(path, 'r')
    jwt = json.load(file)
    file.close()
    return jwt


def dump_jwt(path: str, jwt: dict) -> None:
    """

    :param path: str file path to the jwt.json file
    :param jwt: dict the JWT containing an access token and refresh token
    :return: None
    """

    file = open(path, 'w')
    jwt['expires_at'] = int(time.time()) + jwt.get('expires_in', 1199)
    json.dump(jwt, file)
    file.close()
