from datetime import datetime

from shared_utils.io.json import json_dump

import conf


def save_update(func):
    def wrapped(update, context):
        update_id = str(update['update_id'])
        sub_folder = update_id[:-3]
        now = datetime.now().strftime('%Y-%m-%d__%H-%M-%S')

        filename = f'{conf.data_path}/updates/queue.todo/{sub_folder}/' \
                   f'{update_id}__{now}.json'

        json_dump(filename, update.to_dict())

        return func(update, context)
    return wrapped
