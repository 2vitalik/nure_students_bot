import re
from datetime import datetime

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.api.coda.v2.doc import CodaDoc
from shared_utils.io.json import json_dump

import conf
from bot.commands.register import register_message, register_buttons
from bot.utils.errors import errors
from bot.utils.tg_utils import tg_send


def save_callback_json(query, callback_type):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
    filename = f'{conf.data_path}/callbacks/{callback_type}/{month}/' \
               f'{dt} - {query.id}.json'
    json_dump(filename, query.to_dict())


@errors('callbacks')
def callbacks(update, context):
    bot = context.bot
    query = update.callback_query

    if query.data.startswith('register:'):
        save_callback_json(query, 'register')
        callback_register(bot, query)

    else:
        save_callback_json(query, 'unknown')


def coda_register(username, user_id):
    if not username:
        return False, False

    doc = CodaDoc('d1GDyxjRqoL', coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')
    students = doc.Students.all()

    registered = already_registered = False
    for row in students:
        if row['tg_username'] == f'@{username}':
            if row['tg_id']:
                already_registered = True
                break
            doc.Students.update(row['@id'], {'tg_id': user_id})
            registered = True
            break

    return registered, already_registered


def callback_register(bot, query):
    chat = query.message.chat
    user = query.from_user

    cmd, user_id, username = query.data[len('register:'):].split('|')
    data = '|'.join((user_id, username))

    text = query.message.text_html

    m = re.search(r'<b>Input:</b> (.*)', text)
    if m:
        user_named = m.group(1)
    else:
        tg_send(bot, conf.telegram_error,
                f'⛔️ Не вдалося знайти "Input" у повідомлені')
        return

    m = re.search(r'<b>Full:</b> (.*)', text)
    if m:
        full_name = m.group(1)
    else:
        tg_send(bot, conf.telegram_error,
                f'⛔️ Не вдалося знайти "Full" у повідомлені')
        return

    if cmd == 'process':
        registered, already_registered = coda_register(username, user_id)

        if already_registered:
            icon, title, hidden = '❎', 'Вже був зареєстрован раніше', True
            tg_send(bot, user_id,
                    "❎ Здається, ви вже були зареєстровані раніше!\n"
                    "Можливо, ви відправили запит повторно\n\n"
                    "Якщо це не так, тоді звʼяжіться, будь ласка, "
                    "з викладачем: @vitaliy_lyapota")

        elif registered:
            icon, title, hidden = '✅', 'Зареєстровано автоматично', True
            tg_send(bot, user_id,
                    "✅ Дякую, Ви були успішно зареєстровані :)")

        else:
            icon, title, hidden = '⛔️', 'Не вдалося автоматично', False
            tg_send(bot, conf.telegram_error,
                    f'⛔️ Не вдалося знайти: @{username}')

    elif cmd == 'manually':
        icon, title, hidden = '✅', 'Зареєстровано власноруч', True
        tg_send(bot, user_id,
                "✅ Дякую, Ви були успішно зареєстровані!")

    elif cmd == 'duplicated':
        icon, title, hidden = '❎', 'Це повтор', True
        tg_send(bot, user_id,
                "❎ Здається, ви вже були зареєстровані раніше\n"
                "Можливо, ви відправили запит повторно\n\n"
                "Якщо це не так, тоді звʼяжіться, будь ласка, "
                "з викладачем: @vitaliy_lyapota")

    elif cmd == 'already':
        icon, title, hidden = '✅', 'Вже зареєстровано', True

    elif cmd == 'hide':
        icon, title, hidden = '✔️', 'Приховано', True

    elif cmd == 'show':
        icon, title, hidden = '🔆', 'Знову показано', False

    else:
        tg_send(bot, conf.telegram_error,
                "Register callback has wrong command information\n"
                f"Query Data: {query.data}")
        return

    text = register_message(icon, title,
                            user_id, username, user_named, full_name)

    tg.callback(query, text, register_buttons(data, hidden=hidden))
