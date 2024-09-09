from django.conf import settings
import smtplib
from smtplib import SMTPConnectError

class Email:
    def __init__(self):
        try:
            self.server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            self.server.ehlo()
            self.email = settings.EMAIL_HOST_USER
            self.password = settings.EMAIL_HOST_PASSWORD
            self.server.login(self.email, self.password)
            print("Logged in successfully")
        except SMTPConnectError as e:
            print(f'Something went wrong...\n {e}')

    # send email method
    def send_email(self, to_email_address, email_subject, email_body):
        email_text = f"""\
        From: {self.email}
        To: {to_email_address}
        Subject: {email_subject}

        {email_body}
        """

        try:
            self.server.sendmail(self.email, to_email_address, email_text)
            self.server.close()
            print('Email sent!')
        except:
            print('Something went wrong...')


#APP_PASSWORD = "hcur afvo acrh pjje"