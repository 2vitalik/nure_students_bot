from shared_utils.api.coda.v2.doc import CodaDoc

import conf
from tools.errors import errors
from tools.tg_utils import tg_send


command = 'coda_update'


@errors(command)
def coda_update(update, context):
    bot = context.bot
    chat = update.message.chat

    if chat.id != conf.telegram_admin:  # todo: implement as decorator?
        tg_send(bot, chat.id, '🤷🏻‍♂️ Потрібен адмінський доступ')
        return

    text = update.message.text.strip()
    if not text.startswith(f'/{command} '):  # todo: implement as decorator?
        tg_send(bot, conf.telegram_error,
                f"<b>Error in command</b>\n"
                f"Your input: {text}\n"
                f"Should start from: /{command}")
        return

    coda_doc = text[len(f'/{command} '):].strip()  # todo: implement as decorator?

    tg_send(bot, chat.id, f'🌀 <code>{coda_doc}</code> — updating...')

    doc = CodaDoc(conf.coda_docs[coda_doc], coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')
    doc.update_structure()

    tg_send(bot, chat.id, f'✔️ <code>{coda_doc}</code> — updated')
