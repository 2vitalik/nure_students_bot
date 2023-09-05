from shared_utils.api.coda.v2.doc import CodaDoc

import conf
from tools.errors import errors
from tools.save_update import save_update
from tools.tg import tg_send


command = 'coda_update'


@errors(command)
@save_update
def coda_update(update, context):
    bot = context.bot
    chat = update.message.chat

    if chat.id != conf.telegram_admin:  # todo: implement as decorator?
        tg_send(chat.id, '🤷🏻‍♂️ Потрібен адмінський доступ')
        return

    text = update.message.text.strip()
    if not text.startswith(f'/{command} '):  # todo: implement as decorator?
        tg_send(conf.telegram_error,
                f"<b>Error in command</b>\n"
                f"Your input: {text}\n"
                f"Should start from: /{command}")
        return

    coda_slug = text[len(f'/{command} '):].strip()  # todo: implement as decorator?

    tg_send(chat.id, f'🌀 <code>{coda_slug}</code> — updating...')

    doc = CodaDoc(conf.coda_docs[coda_slug], coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')
    doc.update_structure()

    tg_send(chat.id, f'✔️ <code>{coda_slug}</code> — updated')
