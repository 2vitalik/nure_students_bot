import up  # to go to root folder

from shared_utils.io.json import json_load, json_dump

import conf
from tools.coda import coda_doc
from tools.data import sorted_by_keys


def pull_from_coda(table_slug, coda_table):
    rows = {}
    for row in coda_table.all():
        row_id = row['@id']
        columns = coda_table.overridden.values()
        rows[row_id] = {
            column: row[column]
            for column in columns
        }

    filename = conf.coda_json_path / 'tables' / f'{table_slug}.json'
    json_dump(filename, sorted_by_keys(rows))


def pull_all_from_coda():
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

    for table_slug, coda_table in tables.items():
        pull_from_coda(table_slug, coda_table)


def update_tg_json(filename):
    coda_table = json_load(conf.coda_json_path / 'tables' / filename)

    tg_json = {}
    for row_id, coda_row in coda_table.items():
        tg_id = coda_row['telegram_id']
        tg_id_str = str(tg_id)
        if not tg_id:
            continue
        if tg_id in tg_json:
            raise Exception(f'Error: Duplicated `tg_id`: {tg_id} '
                            f'for the file: {filename}')

        tg_data = {'row_id': row_id, **coda_row}
        del tg_data['telegram_id']

        tg_json[tg_id_str] = tg_data

    json_dump(conf.coda_json_path / 'tg_jsons' / filename,
              sorted_by_keys(tg_json))


def update_all_tg_jsons():
    filenames = [
        'teachers.json',
        'students.json',
        'tg_users.json',
        'tg_chats.json',
        'chats_stream.json',
        'chats_group.json',
        'chats_other.json',
    ]

    for filename in filenames:
        update_tg_json(filename)


if __name__ == '__main__':
    pull_from_coda()
    update_tg_jsons()
