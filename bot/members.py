from os.path import join

from shared_utils.io.io import append
from shared_utils.io.json import json_dump

import conf
from tools.errors import errors
from tools.save_update import save_update
from tools.tg import tg_send


@errors('members')
@save_update
def members(update, context):
    append(join(conf.data_path, 'members.txt'), update.to_json())

    update_id = update['update_id']
    json_dump(f'{conf.data_path}/members/json/{update_id}.json',
              update.to_dict())

    message = update['message'].to_dict()
    chat_id = message['chat']['id']

    if 'new_chat_members' in message:
        for user in message['new_chat_members']:
            process_case(context.bot, chat_id, user, 'new')

    if 'left_chat_member' in message:
        user = message['left_chat_member']
        process_case(context.bot, chat_id, user, 'left')


def process_case(bot, chat_id, user, action):
    chat_slug = conf.chats_slugs.get(chat_id, chat_id)

    telegram_id = user['id']
    first_name = user['first_name']
    username = user.get('username', '')
    last_name = user.get('last_name', '')

    if action == 'new':
        message = f'➕ Joined to: <code>{chat_slug}</code>\n\n'
    elif action == 'left':
        message = f'❌ Left from: <code>{chat_slug}</code>\n\n'
    else:
        raise Exception(f'Unknown `action` value: "{action}"')

    message += \
        f'<b>First:</b> {first_name}\n' \
        f'<b>Last:</b> {last_name}\n\n' \
        f'<b>ID:</b> <code>{telegram_id}</code>,' \
        f' <b><a href="tg://user?id={telegram_id}">Link</a></b>\n' \
        f'<b>Nick:</b> @{username}'

    tg_send(conf.telegram_members, message)
