from datetime import datetime

from shared_utils.io.json import json_dump

import conf
from tools.save_update import save_update
from tools.errors import errors
from tools.tg import tg_send


@errors('messages')
@save_update
def messages(update, context):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d_%H-%M-%S')

    message = update.message or update.edited_message

    chat_id = message.chat_id
    user_id = message.from_user.id
    update_id = update.update_id

    if chat_id == user_id:
        folder = 'bot'
        tg_send(chat_id,
                '🤷🏻‍♂️ Інтерфейс взаємодії з ботом поки що не реалізован')
    else:
        folder = 'group'

    filename = f'{conf.data_path}/messages/input/all/{folder}/{month}/' \
               f'{chat_id}/{dt} - {user_id} - {update_id}.json'
    json_dump(filename, message.to_dict())
