from datetime import datetime

from AuthDatabaseObject import AuthDatabaseObject
from security_password_hashing import generate_encrypted_hash


class Auth:
    def __init__(self, dbo: AuthDatabaseObject):
        self.__database = dbo.connect_db()
        self.__cursor = self.__database.cursor()

    def __execute(self, query: str) -> None:
        self.__cursor.execute(query)

    def check_if_exists(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        self.__execute(query)
        return len(self.__cursor.fetchall()) == 0

    def login(self, username, password):
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{generate_encrypted_hash(password)}'"
        self.__execute(query)
        info = self.__cursor.fetchone()
        return info

    def signup(self, username, password):
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{generate_encrypted_hash(password)}')"
        self.__execute(query)
        self.__database.commit()

    def log(self, ip, type):
        query = f"INSERT INTO iplog (ip, timestamp, type) VALUES ('{ip}', '{datetime.utcnow()}', '{type}')"
        self.__execute(query)
        self.__database.commit()

    def check_log_in_status(self, username):
        query = f"SELECT token FROM log_in_sessions WHERE username = '{username}'"
        self.__execute(query)
        values = self.__cursor.fetchall()
        return values[-1][0]

    def add_log(self, username, ip, token):
        query = f"INSERT INTO log_in_sessions VALUES ('{username}','{token}','{datetime.utcnow()}','{ip}')"
        self.__execute(query)
        self.__database.commit()

    def change_password(self, username, old_password, new_password):
        if self.login(username, old_password):
            query = f"UPDATE users SET password = '{generate_encrypted_hash(new_password)}' WHERE username = '{username}'"
            self.__execute(query)
            self.__database.commit()
            return 200
        else:
            return 403

    def reset_password(self,username ,new_password):
        query = f"UPDATE users SET password = '{generate_encrypted_hash(new_password)}' WHERE username = '{username}'"
