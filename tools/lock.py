import time
from os.path import join

from shared_utils.io.lock.exceptions import LockError, UnlockError
from shared_utils.io.lock.lock_file import lock_file, unlock_file

import conf
from tools.tg import tg_send


def locker(slug):
    def decorator(func):
        def wrapped(*args, **kwargs):
            lock_path = join(conf.lock_path, slug)

            for delta in [0, 1, 2, 4, 8, 16]:
                try:
                    time.sleep(delta)
                    lock_file(lock_path)
                except LockError:
                    pass
                else:
                    break
            else:
                tg_send(conf.telegram_admin, f'LockError: {slug}')
                return

            try:
                return func(*args, **kwargs)
            finally:
                try:
                    unlock_file(lock_path)
                except UnlockError:
                    tg_send(conf.telegram_admin, f'UnlockError: {slug}')

        return wrapped
    return decorator
