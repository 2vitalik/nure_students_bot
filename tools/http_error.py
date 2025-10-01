import time

from requests import HTTPError


def retry_on_http_error(func):
    pause = 1
    while True:
        try:
            return func()
        except HTTPError as e:
            print(f'> Wait {pause} seconds...')
            time.sleep(pause)
            pause *= 2


def a():
    raise HTTPError('test', 400, 'msg', '...', None)

if __name__ == '__main__':
    retry_on_http_error(
        lambda: a()
    )
