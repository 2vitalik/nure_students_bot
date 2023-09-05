from datetime import datetime

from shared_utils.io.json import json_dump

import conf
from tools.errors import errors
from tools.tg import tg_send


@errors('messages')
def messages(update, context):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')

    message = update.message or update.edited_message

    chat_id = message.chat_id
    user_id = message.from_user.id
    update_id = update.update_id

    def get_filename(folder):
        return f'{conf.data_path}/messages/input/all/{folder}/{month}/' \
               f'{chat_id}/{dt} - {user_id} - {update_id}.json'

    if chat_id != user_id:
        json_dump(get_filename('group'), message.to_dict())
        return

    json_dump(get_filename('bot'), message.to_dict())

    tg_send(chat_id, '🤷🏻‍♂️ Інтерфейс взаємодії з ботом поки що не реалізован')
