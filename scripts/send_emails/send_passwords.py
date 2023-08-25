import smtplib
import time

from shared_utils.io.io import read_lines

import conf


def get_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(conf.email_from, conf.email_pass)
    return server


def send_passwords(subject, content, passwords_filename,
                   additional_emails=None):
    server = get_server()
    additional_emails = additional_emails or []

    lines = read_lines(passwords_filename)

    # перший рядок - просто заголовок!
    for line in lines[1:]:
        if not line:
            continue

        name, email, login, password = line.split('\t')
        print(name, email)

        new_content = content.\
            replace('{name}', name).\
            replace('{login}', login).\
            replace('{password}', password)

        emails = [email] + additional_emails

        message = (f'From: {conf.email_from}\n'
                   f'To: {", ".join(emails)}\n'
                   f'Subject: {subject}\n\n'
                   f'{new_content}')
        # print(message)

        server.sendmail(conf.email_from, emails, message.encode('utf-8'))

        print(f"Email {email} was sent.\n")

        time.sleep(1)
