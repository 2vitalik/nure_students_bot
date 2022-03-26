import shared_utils.api.telegram.telegram_utils as tg

from src.utils.tg import basic_handler


class TextHandler:
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
        self.msg = self.send('🤷🏻‍♂️ Интерфейс взаимодействия пока не доступен')
