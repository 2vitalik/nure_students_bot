import up  # to go to root folder

from shared_utils.io.json import json_load, json_dump

import conf
from tools.coda import coda_doc


def pull_from_coda():
    tables = {
        'students': coda_doc.Students,
        'teachers': coda_doc.Teachers,
        'tg_users': coda_doc.TelegramUsers,
        'tg_forums': coda_doc.TelegramForums,
        'tg_groups': coda_doc.TelegramGroups,
        'tg_chats': coda_doc.TelegramChats,
    }
    rows = {}
    for table_slug, table in tables.items():
        rows[table_slug] = {}
        for row in table.all():
            row_id = row['@id']
            columns = table.overridden.values()
            rows[table_slug][row_id] = {
                column: row[column]
                for column in columns
            }
        filename = conf.coda_json_path / 'tables' / f'{table_slug}.json'
        json_dump(filename, rows[table_slug])


def update_tg_jsons():
    files = [
        'students.json',
        'teachers.json',
        'tg_chats.json',
        'tg_forums.json',
        'tg_groups.json',
        'tg_users.json',
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
