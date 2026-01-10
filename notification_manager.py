import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv()

class NotificationManager:
    def __init__(self):
    
        self.twilio_account_sid = os.environ.get("twilio_account_sid")
        self.twilio_account_token = os.environ.get("twilio_account_token")
        self.twilio_num = os.environ.get("TWILIO_NUM")
        self.whatsapp_num = os.environ.get("WHATSAPP_NUM")
        self.client = Client(self.twilio_account_sid, self.twilio_account_token)
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.password = os.environ.get("APP_PASSWORD")
        
    
    def send_message(self, price, date, to_city):
        self.message = self.client.messages.create(
            body=f"Low price alert! Only ${price} to fly from LON to {to_city}, on {date}",
            from_=f"whatsapp:{self.twilio_num}",
            to=f"whatsapp:{self.whatsapp_num}"
        )

    def send_email(self, email, price, to_city, date):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(self.email_address, self.password)
            connection.sendmail(
                from_addr=self.email_address,
                to_addrs=email,
                msg=f"Low price alert! Only ${price} to fly from LON to {to_city}, on {date}"
            )