import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC19ac143574cb2d7ec98fc7f98c0dd92c'
auth_token = '7a2341a34d1a22a38d66e6f8418de7b7'
client = Client(account_sid, auth_token)

service = client.verify.services.create(
                                     friendly_name='My First Verify Service'
                                 )

print(service.sid)