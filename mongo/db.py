from pymongo import MongoClient

import conf
from mongo.collections.tg_polls import TelegramPollsCollection
from mongo.collections.tg_polls_answers import TelegramPollsAnswersCollection
from mongo.collections.tg_polls_history import TelegramPollsHistoryCollection
from mongo.collections.tg_updates import TelegramUpdatesCollection


class MongoDB:
    def __init__(self):
        self.client = MongoClient(conf.mongo_cluster)
        self.database = self.client['nure_students']
        self.tg_polls = TelegramPollsCollection(self)
        self.tg_polls_history = TelegramPollsHistoryCollection(self)
        self.tg_polls_answers = TelegramPollsAnswersCollection(self)
        self.tg_updates = TelegramUpdatesCollection(self)


db = MongoDB()
