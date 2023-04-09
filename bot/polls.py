from datetime import datetime

from shared_utils.io.io import append
from shared_utils.io.json import json_dump, json_dumps

import conf


def process_poll(update, context):
    poll = update.poll

    path = f'{conf.data_path}/polls'
    poll_id = poll.id

    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    json_dump(f'{path}/{poll_id}/history/{date}.json', poll.to_dict())
    json_dump(f'{path}/{poll_id}/latest.json', poll.to_dict())

    print(json_dumps(poll.to_dict()))
    print()


def process_poll_answer(update, context):
    poll = update.poll_answer

    path = f'{conf.data_path}/polls'
    poll_id = poll.poll_id
    user_id = poll.user.id
    options = poll.option_ids
    options_str = '[' + ','.join(map(str, options)) + ']'

    date = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    filename = \
        f'{path}/{poll_id}/answers/{date} - {user_id} - {options_str}.json'
    json_dump(filename, poll.to_dict())

    append(f'{path}/{poll_id}/answers.txt',
           f'[{date}] {user_id}: {options_str}')

    print(json_dumps(poll.to_dict()))
    print()
