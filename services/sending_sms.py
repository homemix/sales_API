import africastalking
import os

from django.contrib.messages import success
from dotenv import load_dotenv

load_dotenv()

username = os.getenv('AFRICA_IS_TALKING_USER_NAME')
api_key = os.getenv('AFRICA_IS_TALKING_API')


class SendSMS:
    def __init__(self, username=username, api_key=api_key, message=None, recipient=None):
        # Initialize SDK with username and api_key
        self.username = username
        self.api_key = api_key
        self.recipient = recipient
        self.message = message
        self.success = False
        africastalking.initialize(self.username, self.api_key)

        # Initialize the SMS service
        self.sms = africastalking.SMS

    def send_message_sync(self):
        """Send SMS synchronously"""

        try:
            response = self.sms.send(self.message, [self.recipient])
            self.success = True
            print(f"Message sent successfully: {response}")
        except Exception as e:
            print(f"Error sending message: {e}")

        return success

    def send_message_async(self):
        """Send SMS asynchronously"""
        response_data = {}

        def on_finish(error, response):
            if error is not None:
                raise error
            print(f"Message sent successfully: {response}")
            self.success = True

        try:
            self.sms.send(self.message, [self.recipient], callback=on_finish)
        except Exception as e:
            print(f"Error sending message: {e}")

        return response_data
