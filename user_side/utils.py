# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC19ac143574cb2d7ec98fc7f98c0dd92c'
auth_token = '06c57e6fb3f292c0cf659a2e0d588135'
client = Client(account_sid, auth_token)


def send_sms(user_code, phone_number):
    message = client.messages.create(
                                body=f'Hi user verification code is {user_code}',
                                from_='+12565791863',
                                to= f"+91{phone_number}"
                            )

    print(message.sid)


