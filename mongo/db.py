from pymongo import MongoClient

import conf


class MongoDB:
    def __init__(self):
        self.client = MongoClient(conf.mongo_cluster)
        self.database = self.client['nure_students']


db = MongoDB()
