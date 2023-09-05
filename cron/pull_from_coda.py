import up  # to go to root folder

from shared_utils.io.json import json_load, json_dump

import conf
from tools.coda import coda_doc
from tools.data import sorted_by_keys


def pull_from_coda():
    tables = {
        'teachers': coda_doc.Teachers,
        'students': coda_doc.Students,
        'streams': coda_doc.StudentStreams,
        'groups': coda_doc.StudentGroups,
        'tg_users': coda_doc.TelegramUsers,
        'tg_chats': coda_doc.TelegramChats,
        'chats_stream': coda_doc.TelegramStreamChats,
        'chats_group': coda_doc.TelegramGroupChats,
        'chats_other': coda_doc.TelegramOtherChats,
    }

    for table_slug, table in tables.items():
        rows = {}
        for row in table.all():
            row_id = row['@id']
            columns = table.overridden.values()
            rows[row_id] = {
                column: row[column]
                for column in columns
            }

        filename = conf.coda_json_path / 'tables' / f'{table_slug}.json'
        json_dump(filename, sorted_by_keys(rows))


def update_tg_jsons():
    files = [
        'teachers.json',
        'students.json',
        'tg_users.json',
        'chats_stream.json',
        'chats_group.json',
        'chats_other.json',
    ]

    for file in files:
        coda_table = json_load(conf.coda_json_path / 'tables' / file)

        tg_json = {}
        for row_id, coda_row in coda_table.items():
            tg_id = coda_row['telegram_id']
            if not tg_id:
                continue
            if tg_id in tg_json:
                raise Exception('123')

            tg_data = {'row_id': row_id, **coda_row}
            del tg_data['telegram_id']

            tg_json[tg_id] = tg_data

        json_dump(conf.coda_json_path / 'tg_jsons' / file, tg_json)


if __name__ == '__main__':
    pull_from_coda()
    update_tg_jsons()
