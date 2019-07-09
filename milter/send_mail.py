# you may ask - if this is running on a mail server, why use sendgrid? Because even when you have DKIM, SPF, DMARC
# etc configured, it's still an absolute nightmare to get reliable delivery to gmail, and other big mail providers

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to, subject, url, proof):
    message = Mail(
        from_email='norepy@chainmail.pw',
        to_emails=to
    )
    message.dynamic_template_data = {
        'proof': proof,
        'url': url,
        'mail_title': subject
    }
    message.template_id = 'd-d90a0d615f414298a72fd360e52a9535'
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
