import up  # to go to root folder

from shared_utils.io.json import json_dump

import conf
from tools.coda import coda_doc


def pull_from_coda():
    path = conf.coda_json_path / f'd{coda_doc.doc_id}'

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
        json_dump(path / 'tables' / f'{table_slug}.json', rows[table_slug])


if __name__ == '__main__':
    pull_from_coda()
