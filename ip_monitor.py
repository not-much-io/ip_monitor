import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from requests import get

conf = dict(
    # Any email address
    toEmail='',
    # Google e-mail address
    fromEmail='',
    # Google password
    password=''
)


class Mailer:
    def __init__(self, subject, body):
        self.subject = subject
        self.body = body

    def send_mail(self):
        from_addr = conf['fromEmail']
        to_addr = conf['toEmail']
        password = conf['password']

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = self.subject

        msg.attach(MIMEText(self.body, 'plain'))

        text = msg.as_string()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, text)
        server.quit()


def get_ip():
    return get('https://api.ipify.org').text


if __name__ == '__main__':
    last_ip = ""
    while True:
        curr_ip = get_ip()

        if curr_ip != last_ip:
            newMail = Mailer("External IP has changed.",
                             "New IP: " + curr_ip)
            newMail.send_mail()
            last_ip = curr_ip
            print("Sent new IP: ", curr_ip)
        else:
            print("ZZzz..")
            sleep(3600)
