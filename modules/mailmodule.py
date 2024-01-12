from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formatdate

import configparser

mail_config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),"ini/mail.ini")


mail_config.read(config_path)
EmailSettings = {
            "sender_email": str(mail_config.get("EmailSettings", "sender_email")),
            "sender_password": str(mail_config.get("EmailSettings", "sender_password")),
            "recipient_email": str(mail_config.get("EmailSettings", "recipient_email"))
}
SMTPSettings = {
            "SMTP_SERVER": str(mail_config.get("SMTPSettings", "SMTP_SERVER")),
            "SMTP_PORT": int(mail_config.get("SMTPSettings", "SMTP_PORT"))
}
# Email settings
monitoring_mail = EmailSettings["sender_email"]
monitoring_password = EmailSettings["sender_password"]
admin_mail = EmailSettings["recipient_email"]
# SMTP settings
smtp_server = SMTPSettings["SMTP_SERVER"]
smtp_port = SMTPSettings["SMTP_PORT"]

# Send a warning Mail to the domain
def send_warning_email(sender_email, sender_password, recipient_email, subject, message_body, attachment_path=None):
        print("Connecting to Mail Server...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        print("Logging into monitoring mail...")
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(message_body, 'plain'))
        # Attach a file if specified
        if attachment_path:
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype="pdf")
                attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
                msg.attach(attachment)

        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Sending the mail has worked!")
        server.quit()
