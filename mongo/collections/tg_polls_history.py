from datetime import datetime


class TelegramPollsHistoryCollection:
    def __init__(self, db):
        self.db = db
        self.items = db.database['tg_polls_history']

    def add(self, data: dict):
        self.items.insert_one({
            **data,
            'created_at': datetime.now(),
        })
