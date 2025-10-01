from pathlib import Path

coda_token = None  # should be set in `local_conf.py`
coda_doc_id = None  # should be set in `local_conf.py`

mongo_cluster = None  # should be set in `local_conf.py`

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
    # 'oop-22': 123,  # should be set in `local_conf.py`
}

coda_docs = {
    'oop-22': 'd1GDyxjRqoL',
    'oop-23': 'dGBWPSQDIDf',
    'debug': 'd1GDyxjRqoL',
    'python-24': 'd-Z4YDpzcFf',
}

coda_tables = {
    'oop-22': 'Students',
    'oop-23': 'Students',
    'debug': 'Students',
}

email_from = None  # should be set in `local_conf.py`
email_pass = None  # should be set in `local_conf.py`

root_path = Path(__file__).resolve().parent
data_path = root_path / 'data'

try:
    from local_conf import *
except ImportError:
    pass

coda_conf_path = data_path / 'coda_conf'
coda_json_path = data_path / 'coda_json' / f'{coda_doc_id}'
