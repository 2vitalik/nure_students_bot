from os.path import join

from shared_utils.io.io import append

import conf
from bot.utils.errors import errors


@errors('members')
def members(update, context):
    append(join(conf.data_path, 'members.txt'), update.to_json())
