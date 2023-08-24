from pathlib import Path

coda_token = None  # should be set in `local_conf.py`

telegram_token = None  # should be set in `local_conf.py`
telegram_admin = None  # should be set in `local_conf.py`
telegram_error = None  # should be set in `local_conf.py`
telegram_members = None  # should be set in `local_conf.py`

slack_hooks = {  # should be set in `local_conf.py`
    'errors': None,
    'status': None,
    'messages': None,
    'callbacks': None,
}

chats_slugs = {
    # -1000000000000: 'slug',  # should be set in `local_conf.py`
}

chats = {
    # 'ПЗПІ-20-4': -1000000000000,  # should be set in `local_conf.py`
}

poll_threads = {
    # 'oop-22': None,  # should be set in `local_conf.py`
}

coda_docs = {
    'oop-22': 'd1GDyxjRqoL',
    'debug': 'd1GDyxjRqoL',
}

coda_tables = {
    'oop-22': 'Students',
    'debug': 'Students',
}

root_path = Path(__file__).resolve().parent
data_path = root_path / 'data'
coda_conf_path = data_path / 'coda_conf'

try:
    from local_conf import *
except ImportError:
    pass
