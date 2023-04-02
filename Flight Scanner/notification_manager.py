from twilio.rest import Client
import os

class NotificationManager:

    def alert_by_text(self, price, departurecity, departcurecode, arrivalcity, arrivalcode, outbounddate, inbounddate):
        account_env = os.environ.get("account_sid_env")
        account_sid = account_env
        auth_token_env = os.environ.get("auth_token_env")
        auth_token = auth_token_env
        client = Client(account_sid, auth_token)
        my_num_env = os.environ.get("my_num_env")
        message = client.messages.create(
            body=f"Low price alert! Only ${price} to fly from {departurecity}-{departcurecode} to {arrivalcity}-"
                 f"{arrivalcode}, from {outbounddate} to {inbounddate}.",
            from_='+15674065589',
            to=my_num_env,
        )
        print(message.status)