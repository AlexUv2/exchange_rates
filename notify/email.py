import smtplib
from email.mime.text import MIMEText


class Email:
    def __init__(self, credentials: dict):
        self.__login = credentials['login']
        self.__connection = smtplib.SMTP_SSL(host=credentials['host'], port=credentials['port'])
        self.__connection.login(user=credentials['login'], password=credentials['password'])

    def send(self, to, subject: str, message: str, is_html: bool = False):
        if not isinstance(to, str) and not isinstance(to, list):
            raise SendMailMessageError("Unknown argument type 'to' [{}]".format(type(to)))

        subtype = 'plain' if not is_html else 'html'
        msg = MIMEText(_text=message, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = self.__login
        msg['To'] = to if isinstance(to, str) else ",".join(to)

        self.__connection.sendmail(from_addr=self.__login, to_addrs=to, msg=msg.as_string())
        print("[Notify.Email] Message sent successfully to [{}]".format(msg['To']))

    def __del__(self):
        if self.__connection:
            self.__connection.close()


class SendMailMessageError(Exception):
    pass
