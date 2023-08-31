import time
from datetime import datetime

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.io.io import append
from shared_utils.io.json import json_dumps, json_dump
from telegram import Bot
from telegram.error import TimedOut, RetryAfter

import conf


bot = Bot(conf.telegram_token)


def get_filename(chat_id, text, folder):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
    hash_value = str(abs(hash(text)))[:7]
    return f'{conf.data_path}/messages/{folder}/{month}/{chat_id}/' \
           f'{dt} - {chat_id} - {hash_value}.json'


def tg_send(chat_id, text, keyboard=None, buttons=None, silent=False):
    out_filename = get_filename(chat_id, text, 'output')

    line = '-' * 79
    output = f'''
{text}

{line}
{json_dumps(keyboard)}
{line}
{json_dumps(buttons)}
{line}
    '''.strip()
    append(out_filename, output)

    try:
        message = tg.send(bot, chat_id, text, keyboard, buttons, silent)
        append(out_filename, 'SENT')

        msg_filename = get_filename(chat_id, text, 'sent')
        json_dump(msg_filename, message.to_dict())

        return message

    except (TimedOut, RetryAfter) as e:
        # todo:
        # slack_error(f'`tg_send`  *{type(e).__name__}*: {str(e)}\n\n'
        #             f'Pause for 1 minute...\n\n'
        #             f'>chat_id: {chat_id}\n\n'
        #             f'>{add_quote(text)}')
        time.sleep(60)

        message = tg_send(chat_id, text, keyboard, buttons, silent)
        append(out_filename, 'DELAYED SENT')
        return message
