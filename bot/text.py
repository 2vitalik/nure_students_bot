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
                       keyboard=keyboard, buttons=buttons, silent=True)

    def extract_coda_column(self, options):
        p = re.compile(r'\{([^}]+)}')
        m = p.search(options)
        if not m:
            return None, options
        return m.group(1), p.sub('', options)

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
                '23': 10,
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
        keys = ['??'] * len(answers)
        for i, answer in enumerate(answers):
            if '|' in answer:
                key, answer = answer.split('|')
                keys[i], answers[i] = key, answer

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

        coda_column, options = self.extract_coda_column(options)
        print(coda_column)

        chats = self.get_chats(options)
        if not chats:
            self.send('⚠️ Помилка в параметрах')
            return

        poll_ids = {}
        for slug, chat_id in conf.chats.items():
            if slug in chats:
                print('Slug:', slug)
                poll_message = self.bot.send_poll(
                    chat_id, question, answers,
                    is_anonymous=is_anonymous,
                    allows_multiple_answers=allows_multiple,
                    disable_notification=True,
                    message_thread_id=conf.poll_threads.get(slug),
                )
                poll_id = poll_message.poll.id
                poll_ids[slug] = poll_id
                print('Poll:', poll_id)

        polls_info = {
            'question': question,
            'answers': answers,
            'keys': keys,
            'poll_ids': poll_ids,
            'coda_column': coda_column,
        }
        dt = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        filename = f'{conf.data_path}/polls/info/{dt}/info.json'
        json_dump(filename, polls_info)

        self.send('✔️ <i>Опитування відправлені:</i>\n' +
                  '\n'.join([
                      f'<b>{slug}</b>: <code>{poll_id}</code>'
                      for slug, poll_id in poll_ids.items()
                  ]))
