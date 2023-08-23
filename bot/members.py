from os.path import join

from shared_utils.io.io import append
from shared_utils.io.json import json_dump

import conf
from bot.utils.errors import errors


@errors('members')
def members(update, context):
    append(join(conf.data_path, 'members.txt'), update.to_json())

    update_id = update['update_id']
    json_dump(f'{conf.data_path}/members/json/{update_id}.json',
              update.to_dict())
