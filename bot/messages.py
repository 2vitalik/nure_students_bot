from datetime import datetime

from shared_utils.io.json import json_dump

import conf
from tools.errors import errors
from tools.tg_utils import tg_send


@errors('messages')
def messages(update, context):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')

    message = update.message

    chat_id = message.chat_id
    user_id = message.from_user.id
    hash_value = str(abs(hash(message.to_json())))[:7]

    def get_filename(folder):
        return f'{conf.data_path}/messages/input/all/{folder}/{month}/' \
               f'{chat_id}/{dt} - {user_id} - h{hash_value}.json'

    if chat_id != user_id:
        json_dump(get_filename('group'), message.to_dict())
        return

    json_dump(get_filename('bot'), message.to_dict())

    tg_send(context.bot, chat_id,
            '🤷🏻‍♂️ Інтерфейс взаємодії з ботом поки що не реалізован')
