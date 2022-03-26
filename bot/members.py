from os.path import join

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.io.io import append

import conf
from src.utils.tg import basic_handler


class MembersHandler:
    context = None
    bot = None
    update = None
    chat_id = None
    input = None
    msg = None

    def send(self, message, keyboard=None, buttons=None):
        return tg.send(self.bot, self.chat_id, message,
                       keyboard=keyboard, buttons=buttons)

    @basic_handler
    def default(self):
        append(join(conf.data_path, 'members.txt'), self.update.to_json())
