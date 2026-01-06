import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    def __init__(self):
        self.url = "https://api.sheety.co/5045b2d0c914791f25027f99d5619b22/flightDeals/prices/"
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