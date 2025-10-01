import conf
from mongo.db import db
from tools.errors import errors
from tools.save_update import save_update
from tools.tg import tg_send, bot


class P:
    slug: str
    question: str
    options: list[str]
    db_options: list[dict[str, str]]
    is_anonymous: bool
    is_multiple: bool
    is_silent: bool
    is_testing: bool
    chat_ids: list[tuple[int, int | None]]


def get_chat_ids(params, err_chat):
    chat_ids = []
    for param in params:
        if '/' in param:
            chat_slug, thread_slug = param.split('/')
        else:
            chat_slug, thread_slug = param, ''

        if chat_slug not in conf.chats:
            tg_send(err_chat, f'⚠️ Невідомий чат: "{chat_slug}"')
            continue
        else:
            chat_id = conf.chats[chat_slug]

        if thread_slug:
            if chat_slug not in conf.threads:
                tg_send(err_chat, f'⚠️ Немає налаштувань гілок: "{chat_slug}"')
                continue
            if thread_slug not in conf.threads[chat_slug]:
                tg_send(err_chat, f'⚠️ Немає налаштування гілки: "{param}"')
                continue
            thread_id = conf.threads[chat_slug][thread_slug]
        else:
            thread_id = ''

        chat_ids.append((chat_id, thread_id))
    return chat_ids


def send_poll(chat_id, thread_id=''):
    poll_message = bot.send_poll(
        chat_id, P.question, P.options,
        is_anonymous=P.is_anonymous,
        allows_multiple_answers=P.is_multiple,
        disable_notification=P.is_silent,
        message_thread_id=thread_id,
    )
    poll_id = poll_message.poll.id

    data = {
        "id": poll_id,
        "question": P.question,
        "options": P.db_options,
        "is_anonymous": P.is_anonymous,
        "allows_multiple_answers": P.is_multiple,
        "type": "regular",
        "is_closed": False,
        "close_date": None,
        "slug": P.slug,
        "chat_id": chat_id,
        "thread_id": thread_id,
        "testing": P.is_testing,
    }
    db.tg_polls_history.add(data)
    db.tg_polls.add(data)


@errors('poll')
@save_update
def poll(update, context):
    chat = update.message.chat
    cmd = update.message.text.strip()
    data = cmd.replace('/poll', '').strip()

    if chat.id != conf.telegram_admin:
        tg_send(chat.id, '🤷🏻‍♂️ Потрібен адмінський доступ')
        return

    params, P.slug, P.question, *P.options = data.split('\n')
    params = params.split()

    P.db_options = [
        {'text': text}
        for text in P.options
    ]

    P.is_anonymous = '-a' in params
    P.is_multiple = '-m' in params
    P.is_testing = '-t' in params
    P.is_silent = '-s' in params

    params.remove('-a') if P.is_anonymous else ...
    params.remove('-m') if P.is_multiple else ...
    params.remove('-s') if P.is_silent else ...
    params.remove('-t') if P.is_testing else ...

    P.chat_ids = get_chat_ids(params, err_chat=chat.id)

    if P.is_testing:
        send_poll(chat.id)
    else:
        for chat_id, thread_id in P.chat_ids:
            send_poll(chat_id, thread_id)
        tg_send(chat.id, '✔️ Опитування відправлені')
