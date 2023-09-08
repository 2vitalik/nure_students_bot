import traceback
from datetime import datetime

from shared_utils.api.slack.core import post_to_slack
from shared_utils.io.io import append

import conf


def slack_logging(chat, message):
    print(message)

    now = datetime.now()
    day, month, dt = \
        now.strftime('%Y-%m-%d'), \
        now.strftime('%Y-%m'), \
        now.strftime('%Y-%m-%d %H-%M-%S')
    filename = conf.data_path / 'logs' / 'slack' / chat / month / f'{day}.txt'
    append(filename, f'[{dt}]: {message}\n')

    post_to_slack(chat, message)


def slack_updates(message):
    slack_logging('updates', message)


def slack_error(message):
    slack_logging('errors', message)


def simplify_traceback(traceback_text):
    # todo
    return traceback_text


def slack_exception(slug, exc, message_suffix='', send_traceback=True):
    exc_name = type(exc).__name__
    message = f':warning: `{slug}`  *{exc_name}*: {exc}  {message_suffix}'

    traceback_text = simplify_traceback(traceback.format_exc().strip())
    content = f'{message}\n```{traceback_text}```'

    slack_error(content if send_traceback else message)
