import smtplib
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, credentials: dict):
        self._login = credentials['login']
        self._connection = smtplib.SMTP_SSL(host=credentials['host'], port=credentials['port'])
        self._connection.login(user=credentials['login'], password=credentials['password'])

    def send(self, to, subject: str, message: str, is_html: bool = False):
        if not isinstance(to, list) and not isinstance(to, str):
            raise Exception("Unknown argument type 'to' [{}]".format(type(to)))

        subtype = 'plain' if not is_html else 'html'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self._login
        msg['To'] = to if isinstance(to, str) else ",".join(to)

        msg_content = MIMEText(_text=message, _subtype=subtype, _charset='utf-8')
        msg.attach(msg_content)

        with open('plot.png', 'rb') as fp:
            msg_image = MIMEImage(fp.read())
        # Define the image's ID as referenced above
        msg_image.add_header('Content-ID', '<plot>')
        msg.attach(msg_image)

        self._connection.sendmail(from_addr=self._login, to_addrs=to, msg=msg.as_string())
        print(f"[Notification.Email] Message sent successfully to [{msg['To']}]")

    def __del__(self):
        if self._connection:
            self._connection.close()
