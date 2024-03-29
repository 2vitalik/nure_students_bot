from datetime import datetime

from shared_utils.io.io import append
from shared_utils.io.json import json_dump, json_dumps

import conf
from tools.errors import errors
from tools.save_update import save_update


def get_poll_path(poll_id):
    return f'{conf.data_path}/polls/updates/{poll_id}'


@errors('process_poll')
@save_update
def process_poll(update, context):
    poll = update.poll
    path = get_poll_path(poll.id)

    # print(json_dumps(poll.to_dict()))
    # print()

    dt = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    json_dump(f'{path}/history/{dt}.json', poll.to_dict())
    json_dump(f'{path}/latest.json', poll.to_dict())


@errors('process_poll_answer')
@save_update
def process_poll_answer(update, context):
    poll = update.poll_answer
    path = get_poll_path(poll.poll_id)

    # print(json_dumps(poll.to_dict()))
    # print()

    dt = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    user = poll.user.id
    options = '[' + ','.join(map(str, poll.option_ids)) + ']'

    json_dump(f'{path}/answers/{dt} - {user} - {options}.json', poll.to_dict())
    append(f'{path}/answers.txt', f'[{dt}]: {user}: {options}')
