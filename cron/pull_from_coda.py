import up  # to go to root folder

from tools.coda import coda_doc


def pull_from_coda():
    coda_students = coda_doc.Students.all()
    # todo...


if __name__ == '__main__':
    pull_from_coda()
