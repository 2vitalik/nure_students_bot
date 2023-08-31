import conf
from tools.tg import tg_send


def errors(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                message = f'<code>{slug}</code>\n' \
                          f'⚠️ <b>{type(e).__name__}</b>: {str(e)}'
                tg_send(conf.telegram_error, message)
                raise
        return wrapped
    return decorator
