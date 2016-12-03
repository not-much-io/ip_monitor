import smtplib
from time import sleep
from requests import get
from collections import namedtuple

User = namedtuple("User", ("user_name",
                           "password",
                           "application_password"  # For two way auth
                           ))


def send_mail(user_: User, subject_: str, to_address: str) -> None:
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()

    server.login(user_.user_name, user_.application_password)
    server.sendmail(
        user_.user_name,
        to_address,
        "Subject: {}".format(subject_)
    )

    server.quit()


def get_ip() -> str:
    return get('https://api.ipify.org').text


if __name__ == '__main__':
    last_ip: str = None
    user = User("kristo.koert@gmail.com", "", "")

    while True:
        curr_ip = get_ip()

        if curr_ip != last_ip:
            subject = "Router IP has changed: {}.".format(curr_ip)
            send_mail(user, subject, user.user_name)
            last_ip = curr_ip
        else:
            sleep(3600)
