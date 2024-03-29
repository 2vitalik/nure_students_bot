import logging

from telegram import Bot, Update
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    PollHandler, PollAnswerHandler, CallbackQueryHandler, ChatMemberHandler
from shared_utils.conf import conf as shared_conf

import conf
from bot.callbacks import callbacks
from bot.commands.coda_tg import coda_tg
from bot.commands.coda_update import coda_update
from bot.messages import messages
from bot.polls import process_poll, process_poll_answer
from bot.commands.register import register
from bot.text import TextHandler
from bot.members import members
from tools.errors import errors


@errors('start_bot')
def start_bot():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s (%(name)s):  %(message)s'
    )
    shared_conf.slack_hooks = conf.slack_hooks

    bot = Bot(conf.telegram_token)
    bot.send_message(conf.telegram_admin, '💬 Starting the bot...')

    text_handler = TextHandler()

    updater = Updater(token=conf.telegram_token)
    d = updater.dispatcher

    # polls:
    d.add_handler(PollHandler(process_poll))
    d.add_handler(PollAnswerHandler(process_poll_answer))

    # commands:
    d.add_handler(CommandHandler('coda_update', coda_update))
    d.add_handler(CommandHandler('coda_tg', coda_tg))
    d.add_handler(CommandHandler('text', text_handler.text))
    d.add_handler(CommandHandler('vote', text_handler.vote))
    d.add_handler(CommandHandler('register', register))

    # members:
    d.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                 members))
    d.add_handler(MessageHandler(Filters.status_update.left_chat_member,
                                 members))

    # all messages:
    d.add_handler(MessageHandler(Filters.all, messages))
    d.add_handler(ChatMemberHandler(messages, chat_member_types=1))

    # callbacks:
    d.add_handler(CallbackQueryHandler(callbacks))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    print('Bot has successfully started.')
    updater.idle()
    print('Bot has stopped.')


if __name__ == '__main__':
    start_bot()
