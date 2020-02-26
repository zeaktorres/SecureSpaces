from twilio.rest import Client 
import PhoneMessaging.apiKeys as keys

class Message:
    account_sid = keys.account_sid
    auth_token = keys.auth_token
    def __init__(self, message):
        self.message = message    
    def sendMessage(self):
        # Your Account SID from twilio.com/console
        # Your Auth Token from twilio.com/console

        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
            to="+15093080228",
            from_="+12055767590",
            body=self.message)
