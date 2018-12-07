import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

email_address = "mars@marstanjx.com"
email_password = "cFW4Ew9fg5iL"
mail_server = "smtp.ipage.com"
mars_usc_address = (
    Address(display_name='Mars USC', username='jianxuat', domain='usc.edu'),
)


def create_email_message(from_address, to_address, subject, text, html):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(text)
    asparagus_cid = make_msgid()
    msg.add_alternative(html.format(asparagus_cid=asparagus_cid[1:-1]), subtype='html')
    return msg


def send_email(subject, text, html):
    msg = create_email_message(
        from_address=email_address,
        to_address=mars_usc_address,
        subject=subject,
        text=text,
        html=html,
    )

    with smtplib.SMTP(mail_server, port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_address, email_password)
        smtp_server.send_message(msg)
