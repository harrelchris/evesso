import json


class Cache:
    def __init__(self, path: str):
        """Cache object used for reading and writing JWTs to/from disk

        :param path: str path to store JWT.
        """

        self.path = path

    def dump(self, jwt: dict):
        """Write jwt to disk

        :param jwt: dict JWT to write
        """

        file = open(self.path, 'w')
        json.dump(jwt, file)
        file.close()

    def load(self) -> dict:
        """Read JWT from disk

        :return: dict JWT read from disk
        """

        file = open(self.path, 'r')
        jwt = json.load(file)
        file.close()
        return jwt
