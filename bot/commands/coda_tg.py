from shared_utils.api.coda.v2.doc import CodaDoc
from shared_utils.io.json import json_dump

import conf
from tools.errors import errors
from tools.tg_utils import tg_send


command = 'coda_tg'


@errors(command)
def coda_tg(update, context):
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

    coda_slug = text[len(f'/{command} '):].strip()  # todo: implement as decorator?

    tg_send(bot, chat.id, f'🌀 <code>{coda_slug}</code> — loading...')

    doc = CodaDoc(conf.coda_docs[coda_slug], coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')

    table_name = conf.coda_tables[coda_slug]
    users = doc.tables[table_name].all()

    data = {
        row['tg_id']: row['@id']
        for row in users
        if row['tg_id']
    }
    filename = f'{conf.data_path}/coda_tg/{coda_slug}/coda_tg.json'
    json_dump(filename, data)

    tg_send(bot, chat.id, f'✔️ <code>{coda_slug}</code> — loaded')
