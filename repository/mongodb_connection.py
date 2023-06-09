from pymongo import MongoClient
# import os

from config import HOST, PORT

class MongoConnection:
    __instance = None

    @staticmethod
    def get_instance():
        if MongoConnection.__instance is None:
            MongoConnection()
        return MongoConnection.__instance

    def __init__(self):
        if MongoConnection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.mongo_host = HOST #os.environ.get('HOST')
            self.mongo_port = PORT #os.environ.get('PORT')
            self.database_name = 'content'
            self.collection_name = 'courses'
            self.client = MongoClient(self.mongo_host, self.mongo_port)
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            MongoConnection.__instance = self

    def close_connection(self):
        self.client.close()
        MongoConnection.__instance = None
