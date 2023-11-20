from django.core.mail import send_mail
from django.utils.html import format_html
from celery import shared_task
from twilio.rest import Client
from decouple import config


@shared_task()
def send_activation_sms(phone_number, activation_code):
    message = f'Your activation code: {activation_code}'
    account_sid = config('SID')
    auth_token = config('AUTH_TOKEN')
    twilio_sender_phone = config('TWILIO_SENDER_PHONE')

    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=twilio_sender_phone, to=phone_number)


@shared_task()
def send_confirmation_email(email, code):
    activation_url = f'http://16.170.220.27/api/account/activate/?u={code}'

    message = format_html(
        '<h2>Hello, activate your account!</h2>\n'
        'Click on the word to activate'
        "<br><a href={}>{}</a></br>"
        "<p>Don't show it anyone</p>",
        activation_url,
        'CLICK HERE'
    )

    send_mail(
        'Hello, activate your account!',
        '',
        'checkemail@gmail.com',
        [email],
        fail_silently=False,
        html_message=message
    )

