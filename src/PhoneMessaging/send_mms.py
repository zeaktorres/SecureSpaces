from twilio.rest import Client 
#import apiKeys as keys
import PhoneMessaging.apiKeys as keys

class Message:
    account_sid = keys.account_sid
    auth_token = keys.auth_token
    def __init__(self, message):
        self.message = message    
    #url = 'https://firebasestorage.googleapis.com/v0/b/spaces-f099d.appspot.com/o/KJ.jpg?alt=media&token=578077d7-22f9-4ff7-9cfd-976a870f70a1'
    #def sendMessage( url):
    def sendMessage(self, url):
        # Your Account SID from twilio.com/console
        # Your Auth Token from twilio.com/console
        #client = Client(account_sid, auth_token)
        client = Client(self.account_sid, self.auth_token)
        message = client.messages \
        .create(
            body=self.message,
            from_="+12055767590",
            media_url=[url],
            to="+15093080228",
        )
