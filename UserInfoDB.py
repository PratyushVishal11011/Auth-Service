import pymongo


class UserInfoDB:
    def __init__(self):
        self.__db = pymongo.MongoClient("mongodb://db1:27017/")["user_info_database"]

    def add_info(self, info: dict, username: str) -> dict:
        collections = self.__db[username]
        result = collections.insert_one(info)
        return {"id": str(result.inserted_id)}

    def get_user_info(self, username: str):
        collections = self.__db[username]
        result = collections.find({"username": username}, {"_id":0})
        return result
