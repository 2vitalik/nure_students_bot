from datetime import datetime

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.io.json import json_dump

import conf


def register_message(icon, title, user_id, username, user_named, full_name):
    return (
        f'{icon} <b>{title}</b>\n\n' 
        f'<b>Input:</b> {user_named}\n' 
        f'<b>Full:</b> {full_name}\n\n' 
        f'<b>ID:</b> <code>{user_id}</code>,' 
        f' <b><a href="tg://user?id={user_id}">Link</a></b>\n' 
        f'<b>Nick:</b> @{username}'
    )


def register_buttons(data, hidden=False):
    if hidden:
        return [
            [
                ('Повернути опції реєстрації', f'register:show|{data}'),
            ],
        ]

    return [
        [
            ('✅ Зареєструвати', f'register:process|{data}'),
            ('✅ Власноруч', f'register:manually|{data}'),
        ],
        [
            ('✔️ Зареєстровано', f'register:already|{data}'),
            ('❎ Це повтор', f'register:duplicated|{data}'),
        ],
        [
            ('Приховати опції реєстрації', f'register:hide|{data}'),
        ]
    ]


def register(update, context):
    bot = context.bot
    chat = update.message.chat
    user = update.message.from_user

    if chat.id != user.id:
        tg.send(bot, chat.id,
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

    cmd = update.message.text.strip()
    if not cmd.startswith('/register'):
        tg.send(bot, conf.telegram_error,
                "Register command started not from /register, that's strange\n"
                f"Command: {cmd}\n"
                f"User: {user.id}")
        tg.send(bot, chat.id,
                "⚠️ Внутрішня помилка у боті, зверніться, будь ласка, "
                "до розробника: @vitaliy_lyapota")
        return

    user_named = cmd[len('/register '):].strip()
    full_name = user.full_name
    data = f'{user.id}|{user.username}'

    text = register_message('⭐️', 'Запит на реєстрацію',
                            user.id, user.username, user_named, full_name)

    try:
        tg.send(bot, conf.telegram_admin, text, buttons=register_buttons(data))
        # todo: process if too many messages at the same minute...

        tg.send(bot, chat.id, "☑️ Запит на реєстрацію відправлено\n"
                              "⏱ Очикуйте підтвердження від викладача")
    except Exception as e:
        tg.send(bot, chat.id,
                "⚠️ Нажаль, сталась якась помилка у роботі бота...\n\n"
                "Зверніться, будь ласка, до розробника: @vitaliy_lyapota")
        tg.send(bot, conf.telegram_error,
                "Unexpected error while sending register message:\n"
                f"{type(e).__name__}: {e}")
