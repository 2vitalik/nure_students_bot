import re
from datetime import datetime

import shared_utils.api.telegram.telegram_utils as tg
from shared_utils.io.json import json_dump

import conf
from src.utils.tg import basic_handler, tg_send


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

    def get_chats(self, options):
        options = options.strip()
        if options[0] != '[' or options[-1] != ']':
            return
        options = options[1:-1]

        chats = []
        slugs = options.split(', ')

        for slug in slugs:

            m = re.fullmatch(r'\d\d-\d{1,2}', slug)
            if m:
                chats.append(f'ПЗПІ-{slug}')
                continue

            groups_count = {
                '19': 11,
                '20': 10,
                '21': 11,
                '22': 10,
            }
            if slug in groups_count:
                chats.extend([
                    f'ПЗПІ-{slug}-{num}'
                    for num in range(1, groups_count[slug] + 1)
                ])
                continue

            chats.append(slug)

        return chats

    @basic_handler
    def text(self):
        if self.chat_id != conf.telegram_admin:
            self.msg = self.send('🤷🏻‍♂️ Потрібен адмінський доступ')
            return

        data = self.input.replace('/text', '')
        options, text = data.split('\n', maxsplit=1)
        chats = self.get_chats(options)
        if not chats:
            self.send('⚠️ Помилка в параметрах')
            return

        for group, chat_id in conf.chats.items():
            if group in chats:
                print(group)
                tg_send(chat_id, text)
        self.send('✔️ Текст відправлено')

    @basic_handler
    def vote(self):
        if self.chat_id != conf.telegram_admin:
            self.msg = self.send('🤷🏻‍♂️ Потрібен адмінський доступ')
            return

        data = self.input.replace('/vote', '')
        options, question, *answers = data.split('\n')

        is_anonymous = False
        if 'a+' in options:
            is_anonymous = True
            options = options.replace('a+', '')
        elif 'a-' in options:
            options = options.replace('a-', '')

        allows_multiple = False
        if 'm+' in options:
            allows_multiple = True
            options = options.replace('m+', '')
        elif 'm-' in options:
            options = options.replace('m-', '')

        chats = self.get_chats(options)
        if not chats:
            self.send('⚠️ Помилка в параметрах')
            return

        for group, chat_id in conf.chats.items():
            if group in chats:
                print(group)
                self.bot.send_poll(chat_id, question, answers,
                                   is_anonymous=is_anonymous,
                                   allows_multiple_answers=allows_multiple)
        self.send('✔️ Опитування відправлено')

    @basic_handler
    def default(self):
        now = datetime.now()
        month, dt = now.strftime('%Y-%m'), now.strftime('%Y-%m-%d %H-%M-%S')
        text = self.update.message.text.strip()
        hash_value = str(abs(hash(text)))[:7]

        chat_id = self.update.message.chat_id
        user_id = self.update.message.from_user.id

        def get_filename(folder):
            return f'{conf.data_path}/messages/input/text/{folder}/{month}/' \
                   f'{chat_id}/{dt} - {user_id} - {hash_value}.json'

        if chat_id != user_id:
            json_dump(get_filename('group'), self.update.message.to_dict())
            return

        json_dump(get_filename('bot'), self.update.message.to_dict())

        self.msg = self.send('🤷🏻‍♂️ Інтерфейс взаємодії з ботом поки що '
                             'не реалізован')
