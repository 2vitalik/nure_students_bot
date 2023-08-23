
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

threads = {
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

data_path = 'data'

try:
    from local_conf import *
except ImportError:
    pass
