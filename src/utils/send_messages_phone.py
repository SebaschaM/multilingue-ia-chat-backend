# from twilio.rest import Client

# account_sid = "AC1b5c8f2914676a03644ba987c33f572e"
# auth_token = "2d6090702781628a46fca32c3e7d18ee"
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     from_="+19897501617", body="Mensaje de  prueba", to="+51979225922"
# )

# print(message.sid)
# # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure
# account_sid = "AC1b5c8f2914676a03644ba987c33f572e"
# auth_token = "2d6090702781628a46fca32c3e7d18ee"
# verify_sid = "VA2eae0af002cd16a3383567a807e28ac5"
# verified_number = "+51917251229"

# client = Client(account_sid, auth_token)

# verification = client.verify.v2.services(verify_sid).verifications.create(
#     to=verified_number, channel="sms"
# )
# print(verification.status)

# otp_code = input("Please enter the OTP:")

# verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
#     to=verified_number, code=otp_code
# )
# print(verification_check.status)
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = "AC1b5c8f2914676a03644ba987c33f572e"
# auth_token = "2d6090702781628a46fca32c3e7d18ee"
# client = Client(account_sid, auth_token)

# message = client.messages.create(
#     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#     from_=+19897501617,
#     messaging_service_sid="MG5d58fa30030e84693b02f8a2307afb58",
#     to="+51979225922",
# )

# print(message.sid)


from twilio.rest import Client

account_sid = "AC1b5c8f2914676a03644ba987c33f572e"
auth_token = "2d6090702781628a46fca32c3e7d18ee"
client = Client(account_sid, auth_token)

message = client.messages.create(to="+51979225922")

print(message.sid)
