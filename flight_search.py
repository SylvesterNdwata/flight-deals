import os
from dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv()

class FlightSearch:
    def __init__(self):
        self.amadeus_api_secret = os.environ.get("amadeus_api_secret")
        self.amadeus_api_key = os.environ.get("amadeus_api_key")
        self.token = os.environ.get("amadeus_access_token")

    
    def get_iata_code(self, city):
        self.url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        
        self.headers = {
            "Authorization": self.token
        }
        
        parameters = {
            "keyword": city,
            "max": 1
        }
        
        self.response = requests.get(url=self.url, params=parameters, headers=self.headers)
        self.codes = self.response.json()
        
        if "error" in self.codes or self.response.status_code == 401 or "errors" in self.codes:
            new_token = self.get_new_token()
            self.token = f"Bearer {new_token['access_token']}"
            os.environ["amadeus_access_token"] = self.token
            self.headers["Authorization"] = self.token
            
            self.response = requests.get(url=self.url, params=parameters, headers=self.headers)
            self.codes = self.response.json()
        
        if "data" not in self.codes or len(self.codes["data"]) == 0:
            return "EMPTY"
        else:
            return self.codes["data"][0]["iataCode"]
    
    def get_new_token(self):
        self.url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        self.token = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api_key,
            "client_secret": self.amadeus_api_secret
        }
        self.response = requests.post(url=self.url, headers=self.headers, data=self.token)
        return self.response.json()
    
    