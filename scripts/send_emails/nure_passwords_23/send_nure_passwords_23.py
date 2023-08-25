from shared_utils.io.io import read, read_lines

from scripts.send_emails.send_passwords import send_passwords


def send_nure_passwords_23():
    groups = [
        '23-3',
        '23-5',
        '23-6',
        '23-7',
        '23-8',
        '23-9',
    ]

    subject = read('text/subject.text')
    content = read('text/content.text')

    for group in groups:
        print(group)
        print()

        group_kurator = read(f'{group}/group_kurator.text').strip()
        new_content = content.replace('{group_kurator}', group_kurator)

        passwords_filename = f'{group}/nure_passwords_{group}.text'

        additional_emails = \
            list(filter(None, read_lines(f'{group}/additional_emails.text')))

        send_passwords(subject, new_content, passwords_filename,
                       additional_emails)


if __name__ == '__main__':
    send_nure_passwords_23()
