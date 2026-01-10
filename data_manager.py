import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self):
        self.url = "https://api.sheety.co/5b0c2b09839e2540abf1b693aef17cd4/flightDeals/prices"
        self.sheety_email_url = os.environ.get("sheety_emails_url")
        self.headers = {
            "Authorization": os.environ.get("sheety_auth")
        }
    
    def get_sheet_data(self):
        self.response = requests.get(self.url, headers=self.headers)
        self.data = self.response.json()
        return self.data["prices"]
        
    def update_iata_codes(self, iatacode, id):
        self.params = {
            "price": {
                "iataCode": iatacode
            }
        }
        
        self.response = requests.put(url=f"{self.url}/{id}", json=self.params, headers=self.headers)
        return self.response.json()
    
    def update_flight_price(self, price, id):
        self.params = {
            "price": {
                "lowestPrice": price
            }
        }
        
        self.response = requests.put(url=f"{self.url}/{id}", json=self.params, headers=self.headers)
        return self.response.json()
    
    def get_customer_emails(self):
        sheety_emails_url = self.sheety_email_url
        self.response = requests.get(url=sheety_emails_url, headers=self.headers)
        self.emails = self.response.json()
        self.user_emails = [user["whatIsYourEmailAddress?"] for user in self.emails["users"]]
        return self.user_emails