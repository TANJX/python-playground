from email.headerregistry import Address
from email.message import EmailMessage
import smtplib

email_address = "mars@marstanjx.com"
email_password = "cFW4Ew9fg5iL"
mail_server = "smtp.ipage.com"
mars_usc_address = (
    Address(display_name='Mars USC', username='jianxuat', domain='usc.edu'),
)


def create_email_message(from_address, to_address, subject, body):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)
    return msg


def send_email(subject, body):
    msg = create_email_message(
        from_address=email_address,
        to_address=mars_usc_address,
        subject=subject,
        body=body,
    )

    with smtplib.SMTP(mail_server, port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_address, email_password)
        smtp_server.send_message(msg)
