import flask.app
import mysql.connector


class AuthDatabaseObject:
    def __init__(self, app: flask.app.Flask):
        self.__app = app

    def connect_db(self):
        connection = mysql.connector.connect(
            host=self.__app.config['MYSQL_HOST'],
            user=self.__app.config['MYSQL_USER'],
            password=self.__app.config['MYSQL_PASSWORD'],
            database=self.__app.config['MYSQL_DATABASE']
        )
        return connection



