from telegram import Bot

import conf
from tools.tg import tg_send


bot = Bot(conf.telegram_token)


def errors(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                message = f'<code>{slug}</code>\n' \
                          f'⚠️ <b>{type(e).__name__}</b>: {str(e)}'
                tg_send(bot, conf.telegram_error, message)
                raise
        return wrapped
    return decorator
