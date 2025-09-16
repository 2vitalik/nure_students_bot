import re
from datetime import datetime

from shared_utils.api.coda.v2.doc import CodaDoc
from shared_utils.io.json import json_dump

import conf
from bot.commands.register import register_message, register_buttons
from tools.errors import errors
from tools.save_update import save_update
from tools.telegram_utils import telegram_callback
from tools.tg import tg_send


def save_callback_json(query, callback_type):
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
    filename = f'{conf.data_path}/callbacks/{callback_type}/{month}/' \
               f'{dt} - {query.id}.json'
    json_dump(filename, query.to_dict())


@errors('callbacks')
@save_update
def callbacks(update, context):
    bot = context.bot
    query = update.callback_query

    if query.data.startswith('register:'):
        save_callback_json(query, 'register')
        callback_register(bot, query)

    else:
        save_callback_json(query, 'unknown')


def simplify(name):
    return name.strip().lower().replace('`', 'ʼ').replace("'", 'ʼ').replace('&#x27;', 'ʼ')


def coda_register(user_named, username, user_id):
    if not username:
        return False, False

    doc = CodaDoc(conf.coda_docs['python-24'], coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')
    students = doc.Students.all()

    parts = user_named.split()

    first_name = last_name = patronymic = ''
    if len(parts) == 3:
        last_name, first_name, patronymic = parts
    elif len(parts) == 2:
        last_name, first_name = parts
    # elif len(parts) == 1:
    #     last_name = parts[0]

    last_name = simplify(last_name)
    first_name = simplify(first_name)

    registered = already_registered = False

    for row in students:
        coda_last_name = simplify(row['last_name'])
        coda_first_name = simplify(row['first_name'])
        found = (
            row['tg_username'] == f'@{username}' or
            coda_last_name == last_name and coda_first_name == first_name or
            coda_last_name == first_name and coda_first_name == last_name
        )
        if found:
            if row['tg_id']:
                already_registered = True
                break
            doc.Students.update(row['@id'], {
                'tg_id': user_id,
                'tg_username': f'@{username}',
            })
            registered = True
            break

    return registered, already_registered


def callback_register(bot, query):
    chat = query.message.chat
    user = query.from_user

    # cmd, user_id, username = query.data[len('register:'):].split('|')
    cmd = query.data[len('register:'):]
    # data = '|'.join((user_id, username))

    text = query.message.text_html

    first_line = text.split('\n')[0]
    icon, title = re.search(r'(.*) <b>(.*)</b>', first_line).groups()
    # todo: if m:

    m = re.search(r'<b>Input:</b> (.*)', text)
    if m:
        user_named = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "Input" у повідомлені')
        return

    m = re.search(r'<b>Full:</b> (.*)', text)
    if m:
        full_name = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "Full" у повідомлені')
        return

    m = re.search(r'<b>ID:</b> <code>(.*)</code>,', text)
    if m:
        user_id = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "ID" у повідомлені')
        return

    m = re.search(r'<b>Nick:</b> @(.*)', text)
    if m:
        username = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "ID" у повідомлені')
        return

    if cmd == 'process':
        registered, already_registered = (
            coda_register(user_named, username, user_id))

        if already_registered:
            icon, title, hidden = '🟠', 'Вже був зареєстрован раніше', True
            tg_send(user_id,
                    "❎ Здається, ви вже були зареєстровані раніше!\n"
                    "Можливо, ви відправили запит повторно\n\n"
                    "Якщо це не так, тоді звʼяжіться, будь ласка, "
                    "з викладачем: @vitaliy_lyapota")

        elif registered:
            icon, title, hidden = '✔️', 'Зареєстровано автоматично', True
            tg_send(user_id,
                    "✅ Дякую, Ви були успішно зареєстровані :)")

        else:
            icon, title, hidden = '🔴', 'Не вдалося автоматично', False
            tg_send(conf.telegram_admin,
                    f'🚫 Немає в табличці: \n'
                    f'▪️ "{user_named}"\n'
                    f'▪️ @{username}')

    elif cmd == 'manually':
        icon, title, hidden = '✔️', 'Зареєстровано власноруч', True
        tg_send(user_id,
                "✅ Дякую, Ви були успішно зареєстровані!")

    elif cmd == 'duplicated':
        icon, title, hidden = '➕', 'Це повтор', True
        tg_send(user_id,
                "🟠 Здається, ви вже були зареєстровані раніше\n"
                "Можливо, ви відправили запит повторно\n\n"
                "Якщо це не так, тоді звʼяжіться, будь ласка, "
                "з викладачем: @vitaliy_lyapota")

    elif cmd == 'already':
        icon, title, hidden = '✔️', 'Вже зареєстровано', True

    elif cmd == 'hide':
        hidden = True

    elif cmd == 'show':
        hidden = False

    else:
        tg_send(conf.telegram_admin,
                "Register callback has wrong command information\n"
                f"Query Data: {query.data}")
        return

    text = register_message(icon, title,
                            user_id, username, user_named, full_name)

    telegram_callback(query, text, register_buttons(hidden=hidden))
