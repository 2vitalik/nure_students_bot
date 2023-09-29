import time

from telegram import Bot, ParseMode
from telegram.error import TimedOut, RetryAfter

import conf
# from src.utils.slack import slack_error

bot = Bot(conf.telegram_token)


def add_quote(text):
    return text.replace('\n', '\n> ')


def tg_send(chat_id, text, thread_id=None):  # todo: remove...
    try:
        bot.send_message(chat_id, text,
                         parse_mode=ParseMode.HTML,
                         disable_web_page_preview=True,
                         message_thread_id=thread_id)
    except (TimedOut, RetryAfter) as e:
        # todo:
        # slack_error(f'`tg_send`  *{type(e).__name__}*: {str(e)}\n\n'
        #             f'Pause for 1 minute...\n\n'
        #             f'>chat_id: {chat_id}\n\n'
        #             f'>{add_quote(text)}')
        time.sleep(60)
        return tg_send(chat_id, text)


def basic_handler(func):
    def wrapper(self, update, context):
        self.context = context
        self.bot = context.bot
        self.update = update
        self.chat_id = update.message.chat_id
        self.input = update.message.text.strip() if update.message.text else ''
        return func(self)
    return wrapper
