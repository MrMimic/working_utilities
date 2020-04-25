import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emails(object):
    """
    Work with distant mail services

    :param email: The email to connect to
    :type email: str
    :param password: The associated password
    :type password: str
    :param server: The server to connect
    :type server: str
    :param port: The port used to connect the server
    :type port: int
    """

    def __init__(self, email, password, server, port):

        self.server = smtplib.SMTP(server, port)
        self.server.starttls()
        self.server.login(email, password)

        self.email = email

    def send_mail(self, corresponding, file_name, subject, text):
        """
        Uses server connected into the init to send mails

        :param corresponding: List of email to send mail to
        :type corresponding: list
        :param file_name: Path to the file to join
        :type file_name: str / None
        :param text: The text body
        :type text: str
        """

        for adress in corresponding:  # For each address
            # Write mail
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = adress
            msg['Subject'] = subject
            body = text
            msg.attach(MIMEText(body, 'plain'))
            # Add file
            if file_name is not None:
                attachment = open(file_name, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename = {}'.format(file_name))
                msg.attach(part)
            # Send
            text = msg.as_string()
            self.server.sendmail(self.email, adress, text)
            self.server.quit()
