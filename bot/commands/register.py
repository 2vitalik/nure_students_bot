from datetime import datetime

from shared_utils.io.json import json_dump

import conf
from tools.errors import errors
from tools.save_update import save_update
from tools.tg import tg_send


def register_message(icon, title, user_id, username, user_named, full_name):
    return (
        f'{icon} <b>{title}</b>\n\n' 
        f'<b>Input:</b> {user_named}\n' 
        f'<b>Full:</b> {full_name}\n\n' 
        f'<b>ID:</b> <code>{user_id}</code>,' 
        f' <b><a href="tg://user?id={user_id}">Link</a></b>\n' 
        f'<b>Nick:</b> @{username}'
    )


def register_buttons(hidden=False):
    if hidden:
        return [
            [
                ('Повернути опції реєстрації', f'register:show'),
            ],
        ]

    return [
        [
            ('✅ Зареєструвати', f'register:process'),
            ('✅ Власноруч', f'register:manually'),
        ],
        [
            ('✔️ Зареєстровано', f'register:already'),
            ('❎ Це повтор', f'register:duplicated'),
        ],
        [
            ('Приховати опції реєстрації', f'register:hide'),
        ]
    ]


@errors('register')
@save_update
def register(update, context):
    bot = context.bot
    chat = update.message.chat
    user = update.message.from_user

    cmd = update.message.text.strip()

    if chat.id != user.id:
        tg_send(chat.id,
                '⚠️ Відправляйте запит на реєстрацію не тут, '
                'а в особистому чаті з '
                '<b><a href="https://t.me/nure_students_bot">ботом</a></b>',
                silent=True)
        return

    # Save JSON user information:
    now = datetime.now()
    month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
    filename = f'{conf.data_path}/register/{month}/{dt} - {user.id}.json'
    json_dump(filename, user.to_dict())

    hash_value = str(abs(hash(cmd)))[:7]
    filename = f'{conf.data_path}/messages/input/register/{month}/{chat.id}/' \
               f'{dt} - {user.id} - {hash_value}.json'
    json_dump(filename, update.message.to_dict())

    if not cmd.startswith('/register'):
        tg_send(conf.telegram_error,
                "Register command started not from /register, that's strange\n"
                f"Command: {cmd}\n"
                f"User: {user.id}")
        tg_send(chat.id,
                "⚠️ Внутрішня помилка у боті, зверніться, будь ласка, "
                "до розробника: @vitaliy_lyapota")
        return

    user_named = cmd[len('/register '):].strip()
    full_name = user.full_name
    # data = f'{user.id}|{user.username}|{user_named}'  # fixme: remove unsuccessful attempt
    # print(data)

    text = register_message('⭐️', 'Запит на реєстрацію',
                            user.id, user.username, user_named, full_name)

    try:
        tg_send(conf.telegram_admin, text, buttons=register_buttons())
        # todo: process if too many messages at the same minute...

        if not user_named:
            tg_send(chat.id, "🙏 Краще вказати ПІБ в команді\n"
                             "✔️ Але запит на реєстрацію відправлено\n"
                                  "⏱ Очикуйте підтвердження від викладача")
        elif ' ' not in user_named:
            tg_send(chat.id, "🤔 Схоже, ви не вказали ПІБ в команді\n"
                             "✔️ Але запит на реєстрацію відправлено\n"
                                  "⏱ Очикуйте підтвердження від викладача")
        else:
            tg_send(chat.id, "☑️ Запит на реєстрацію відправлено\n"
                                  "⏱ Очикуйте підтвердження від викладача")

    except Exception as e:
        tg_send(chat.id,
                "⚠️ Нажаль, сталась якась помилка у роботі бота...\n\n"
                "Зверніться, будь ласка, до розробника: @vitaliy_lyapota")
        tg_send(conf.telegram_error,
                "Unexpected error while sending register message:\n"
                f"{type(e).__name__}: {e}")
