import time
from datetime import datetime

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.io.io import append
from shared_utils.io.json import json_dumps
from telegram.error import TimedOut, RetryAfter

import conf


def tg_send(bot, chat_id, text, keyboard=None, buttons=None, silent=False):
    try:
        now = datetime.now()
        month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
        hash_value = str(abs(hash(text)))[:7]
        filename = f'{conf.data_path}/messages/{month}/{chat_id}/' \
                   f'{dt} - {chat_id} - {hash_value}.json'

        line = '-' * 79
        output = f'''
{text}

{line}
{json_dumps(keyboard)}
{line}
{json_dumps(buttons)}
{line}
        '''.strip()
        append(filename, output)

        return tg.send(bot, chat_id, text, keyboard, buttons, silent)
    except (TimedOut, RetryAfter) as e:
        # todo:
        # slack_error(f'`tg_send`  *{type(e).__name__}*: {str(e)}\n\n'
        #             f'Pause for 1 minute...\n\n'
        #             f'>chat_id: {chat_id}\n\n'
        #             f'>{add_quote(text)}')
        time.sleep(60)
        return tg_send(bot, chat_id, text, keyboard, buttons, silent)
