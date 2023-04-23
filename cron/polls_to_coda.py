import json
import os
from os.path import exists
import up  # to go to root folder

from shared_utils.api.coda.v2.doc import CodaDoc
from shared_utils.io.io import read, write
from shared_utils.io.json import json_load

import conf
from bot.polls import get_poll_path
from bot.utils.errors import errors


def get_processed_count(poll_id):
    poll_path = get_poll_path(poll_id)
    filename = f'{poll_path}/processed.txt'

    if not exists(filename):
        return 0

    content = read(filename)
    if not content:
        return 0

    return int(content)


def set_processed_count(poll_id, value):
    poll_path = get_poll_path(poll_id)
    filename = f'{poll_path}/processed.txt'

    write(filename, value)


def get_answers(poll_id, processed):
    poll_path = get_poll_path(poll_id)
    filename = f'{poll_path}/answers.txt'

    if not exists(filename):
        return []

    content = read(filename).strip()
    if not content:
        return []

    lines = [
        line.split(': ')
        for line in content.split('\n')
    ]

    data = [
        (tg_id, json.loads(options))
        for date, tg_id, options in lines
    ]

    return data[processed:]


@errors('polls_to_coda')
def polls_to_coda():
    path = f'{conf.data_path}/polls/info'

    for folder in sorted(os.listdir(path)):
        info = json_load(f'{path}/{folder}/info.json')
        print(info)

        for slug, poll_id in info['poll_ids'].items():
            doc = CodaDoc(conf.coda_docs[slug], coda_token=conf.coda_token,
                          conf_path=f'{conf.data_path}/coda_conf')

            processed = get_processed_count(poll_id)
            print(processed)

            answers = get_answers(poll_id, processed)
            print(answers)
            if not answers:
                continue

            filename = f'{conf.data_path}/coda_tg/{slug}/coda_tg.json'
            coda_tg = json_load(filename)

            table_name = conf.coda_tables[slug]
            table = doc.tables[table_name]
            column = info['coda_column']

            for tg_id, options in answers:
                print(tg_id, options)

                row_id = coda_tg[tg_id]

                new_value = ''.join([
                    info['keys'][i]
                    for i in options
                ])

                table.update(row_id, {column: new_value})

            new_processed = processed + len(answers)
            set_processed_count(poll_id, str(new_processed))


if __name__ == '__main__':
    polls_to_coda()
