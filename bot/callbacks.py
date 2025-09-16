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
from tools.un_translit import lat_to_uk


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


def get_options(name):
    options = [
        part
        for part in name.split()
        if part
    ]

    if len(options) == 1:
        if m := re.match(r'^([A-Z][a-z]+)([A-Z][a-z]+)$', options[0]):
            options = m.groups()

    options = {
        simplify(option)
        for option in options
    }

    options |= {
        lat_to_uk(option)
        for option in options
    }

    return options


def coda_register(user_named, full_name, username, user_id):
    if not username:
        return False, False

    doc = CodaDoc(conf.coda_docs['python-24'], coda_token=conf.coda_token,
                  conf_path=f'{conf.data_path}/coda_conf')
    students = doc.Students.all()

    options = get_options(user_named) | get_options(full_name)

    registered = already_registered = False

    for row in students:
        last_name = simplify(row['last_name'])
        first_name = simplify(row['first_name'])
        found = (
            username and row['tg_username'] == f'@{username}' or
            last_name in options and first_name in options
        )
        if found:
            if row['tg_id']:
                already_registered = True
                break
            doc.Students.update(row['@id'], {
                'tg_id': user_id,
                'tg_username': f'@{username}',
                'tg_registered_at': str(datetime.now()),
            })
            registered = True
            break

    return registered, already_registered


def callback_register(bot, query):
    chat = query.message.chat
    user = query.from_user
    msg_id = query.message.message_id

    # cmd, user_id, username = query.data[len('register:'):].split('|')
    cmd = query.data[len('register:'):]
    # data = '|'.join((user_id, username))

    text = query.message.text_html

    first_line = text.split('\n')[0]
    icon, title = re.search(r'(.*) <b>(.*)</b>', first_line).groups()
    # todo: if m:

    # fixme: Temporary fix to change old icons in existing messages:
    if icon == '✅' and title == 'Зареєстровано автоматично':
        icon = '✔️'
        title = 'Зареєстровано автоматично 🎶'

    m = re.search(r'<b>Input:</b> (.*)', text)
    if m:
        user_named = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "Input" у повідомлені',
                reply_to=msg_id)
        return

    m = re.search(r'<b>Full:</b> (.*)', text)
    if m:
        full_name = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "Full" у повідомлені',
                reply_to=msg_id)
        return

    m = re.search(r'<b>ID:</b> <code>(.*)</code>,', text)
    if m:
        user_id = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "ID" у повідомлені',
                reply_to=msg_id)
        return

    m = re.search(r'<b>Nick:</b> @(.*)', text)
    if m:
        username = m.group(1)
    else:
        tg_send(conf.telegram_admin,
                f'❌ Не вдалося знайти "ID" у повідомлені',
                reply_to=msg_id)
        return

    if cmd in ['reg-auto', 'process']:  # fixme: remove old case 'process'
        registered, already_registered = (
            coda_register(user_named, full_name, username, user_id))

        if already_registered:
            icon, title, hidden = '🟠', 'Вже був зареєстрован раніше 🎶', True
            tg_send(user_id,
                    "🟠 Здається, ви вже були зареєстровані раніше!\n"
                    "Можливо, ви відправили запит повторно\n\n"
                    "Якщо це не так, тоді звʼяжіться, будь ласка, "
                    "з викладачем: @vitaliy_lyapota")

        elif registered:
            icon, title, hidden = '✔️', 'Зареєстровано автоматично 🎶', True
            tg_send(user_id,
                    "✅ Дякую, Ви були успішно зареєстровані :)")

        else:
            icon, title, hidden = '🔴', 'Не вдалося автоматично 🕶', False
            tg_send(conf.telegram_admin,
                    f'🚫 Немає в табличці: \n'
                    f'▪️ "{user_named}"\n'
                    f'▪️ @{username}',
                    reply_to=msg_id)

    elif cmd in ['reg-hand', 'manually']:  # fixme: remove old case 'manually'
        icon, title, hidden = '➕', 'Зареєстровано власноруч 🎶', True
        tg_send(user_id, "✅ Дякую, Ви були успішно зареєстровані!")

    elif cmd in ['reg-copy', 'duplicated']:  # fixme: remove old case 'duplicated'
        icon, title, hidden = '🟠', 'Схоже це дубль? 🎶', True
        tg_send(user_id,
                "🟠 Здається, ви вже були зареєстровані раніше\n"
                "Можливо, ви відправили запит повторно\n\n"
                "Якщо це не так, тоді звʼяжіться, будь ласка, "
                "з викладачем: @vitaliy_lyapota")

    elif cmd in ['hid-auto']:
        icon, title, hidden = '✔️', 'Зареєстровано автоматично 🕶', True

    elif cmd in ['hid-hand']:
        icon, title, hidden = '➕', 'Зареєстровано власноруч 🕶', True

    elif cmd in ['hid-copy']:
        icon, title, hidden = '✖️', 'Схоже це дубль 🕶', True

    elif cmd == 'hide':
        hidden = True

    elif cmd == 'show':
        hidden = False

    else:
        tg_send(conf.telegram_admin,
                "Register callback has wrong command information\n"
                f"Query Data: {query.data}",
                reply_to=msg_id)
        return

    text = register_message(icon, title,
                            user_id, username, user_named, full_name)

    telegram_callback(query, text, register_buttons(hidden=hidden))


if __name__ == '__main__':
    print(get_options('VitaliiLiapota'))
    print(get_options('Vitalii Liapota'))
    print(get_options('Віталій Ляпота'))
