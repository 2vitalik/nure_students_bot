from datetime import datetime


class TelegramPollsAnswersCollection:
    def __init__(self, db):
        self.db = db
        self.items = db.database['tg_polls_answers']

    def add(self, data: dict):
        self.items.insert_one({
            **data,
            'saved_to_coda': False,
            'created_at': datetime.now(),
        })

    def get(self, poll_id: int):
        return self.items.find_one({'id': poll_id})

    def update(self, poll_id: int, data: dict):
        if not self.get(poll_id):
            self.add(data)
            return

        self.items.update_one(
            {'id': poll_id},
            {'$set': {
                **data,
                'updated_at': datetime.now(),
            }})

    def mark_saved(self, _id):
        self.items.update_one(
            {'_id': _id},
            {'$set': {
                'saved_to_coda': True,
            }})

    def get_new(self):
        return self.items.find({'saved_to_coda': False})
