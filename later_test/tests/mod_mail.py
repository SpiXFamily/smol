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

