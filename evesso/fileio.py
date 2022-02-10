import json
import time


def load_jwt(jwt_file_path):
    file = open(jwt_file_path, 'r')
    jwt = json.load(file)
    file.close()
    return jwt


def dump_jwt(jwt_file_path, jwt):
    file = open(jwt_file_path, 'w')
    jwt['expires_at'] = int(time.time()) + jwt.get('expires_in', 1199)
    json.dump(jwt, file)
    file.close()
