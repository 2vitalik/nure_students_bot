import logging

from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    PollHandler, PollAnswerHandler, CallbackQueryHandler
from shared_utils.conf import conf as shared_conf

import conf
from bot.callbacks import callbacks
from bot.polls import process_poll, process_poll_answer
from bot.register import register
from bot.text import TextHandler
from bot.members import MembersHandler


def start_bot():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )
    shared_conf.slack_hooks = conf.slack_hooks

    bot = Bot(conf.telegram_token)
    bot.send_message(chat_id=conf.telegram_admin, text='💬 Starting the bot...')

    text_handler = TextHandler()
    members_handler = MembersHandler()

    updater = Updater(token=conf.telegram_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(PollHandler(process_poll))
    dispatcher.add_handler(PollAnswerHandler(process_poll_answer))
    dispatcher.add_handler(CommandHandler('text', text_handler.text))
    dispatcher.add_handler(CommandHandler('vote', text_handler.vote))
    dispatcher.add_handler(CommandHandler('register', register))
    dispatcher.add_handler(MessageHandler(Filters.text, text_handler.default))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                          members_handler.default))
    dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member,
                                          members_handler.default))
    dispatcher.add_handler(CallbackQueryHandler(callbacks))

    updater.start_polling()
    print('Bot has successfully started.')
    updater.idle()
    print('Bot has finished.')


if __name__ == '__main__':
    start_bot()
