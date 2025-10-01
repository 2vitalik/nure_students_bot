from pprint import pprint

import up  # to go to root folder
from cron.polls.coda_doc import doc
from mongo.db import db
from scripts.db_students.http_error import retry_on_http_error
from tools.errors import errors


index_icons = [
    '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '⏸️'
]


def process_polls():
    for poll in db.tg_polls.get_new():
        print(poll)
        poll_id = str(poll['id'])

        pprint({
                'tg_poll_id': poll_id,
                'question': poll['question'],
                'slug': poll['slug'],
                'chat_id': poll['chat_id'],
                'thread_id': poll['thread_id'],
                'testing': poll['testing'],
            })

        retry_on_http_error(
            lambda: doc.tg_polls.insert({
                'tg_poll_id': poll_id,
                'question': poll['question'],
                'slug': poll['slug'],
                'chat_id': poll['chat_id'],
                'thread_id': poll['thread_id'],
                'testing': poll['testing'],
            })
        )

        # get `row_id` after `insert` to coda:
        # res = requests.post(url, json=payload, headers=hdrs).json()
        # row_id = res["addedRowIds"][0]  # наприклад: "i-ECC1p8uxHE"

        for index, option in enumerate(poll['options']):
            text = option['text']
            icon = text.split()[0]
            retry_on_http_error(
                lambda: doc.tg_options.insert({
                    'tg_poll': poll_id,
                    'option': text,
                    'index': index,
                    'icon': icon,  # index_icons[index],
                })
            )
        db.tg_polls.mark_saved(poll_id)


def process_polls_answers():
    for answer in db.tg_polls_answers.get_new():
        pprint(answer)
        retry_on_http_error(
            lambda: doc.tg_answers.insert({
                'tg_poll': str(answer['poll_id']),
                'tg_user_id': answer['user']['id'],
                'tg_answers': answer['option_ids'],
            })
        )
        db.tg_polls_answers.mark_saved(answer['_id'])


@errors('polls_to_coda')
def polls_to_coda():
    process_polls()
    process_polls_answers()


if __name__ == '__main__':
    polls_to_coda()
