from datetime import datetime


class TelegramUpdatesCollection:
    def __init__(self, db):
        self.db = db
        self.items = db.database['tg_updates']

    def add(self, data: dict):
        self.items.insert_one({
            **data,
            'created_at': datetime.now(),
        })
