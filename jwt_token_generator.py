import datetime

import flask.app
import jwt


class jwt_generator:
    def __init__(self, app: flask.app.Flask):
        self.__SECRET_KEY = app.config["SECRET_KEY"]

    def generate_token(self, username: str, token_type: str = "auth") -> dict:
        token = jwt.encode({
            'username': username,
            "token_type": token_type,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, self.__SECRET_KEY, algorithm='HS512')
        return {"token": token}
