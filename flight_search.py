import os
from dotenv import load_dotenv
import requests
from pprint import pprint
import datetime as dt
from dateutil.relativedelta import relativedelta

load_dotenv()

class FlightSearch:
    def __init__(self):
        self.amadeus_api_secret = os.environ.get("amadeus_api_secret")
        self.amadeus_api_key = os.environ.get("amadeus_api_key")
        self.token = os.environ.get("amadeus_access_token")
        self.today = dt.date.today()
        self.six_months_from_now = self.today + relativedelta(months=6)
        dates = []
        current = self.today
        while current <= self.six_months_from_now:
            dates.append(current)
            current += dt.timedelta(days=1)
        
        self.formatted_dates = [date.strftime("%Y-%m-%d") for date in dates]

    
    def get_iata_code(self, city):
        url = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        
        headers = {
            "Authorization": self.token
        }
        
        parameters = {
            "keyword": city,
            "max": 1
        }

        self.response = requests.get(url=url, params=parameters, headers=headers)
        self.codes = self.response.json()
        
        if self.generate_token_when_error(self.codes, self.response.status_code):
            self.response = requests.get(url=url, params=parameters, headers=headers)
            self.codes = self.response.json()
        
        if "data" not in self.codes or len(self.codes["data"]) == 0:
            return None
        else:
            return self.codes["data"][0]["iataCode"]
    
    def get_new_token(self):
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        self.token = {
            "grant_type": "client_credentials",
            "client_id": self.amadeus_api_key,
            "client_secret": self.amadeus_api_secret
        }
        self.response = requests.post(url=url, headers=headers, data=self.token)
        return self.response.json()
    
    def get_cheap_flights(self, city_iatacode):
        self.cheapest_price = None
        for date in self.formatted_dates:
            conditions = (
                 not city_iatacode or
                 len(city_iatacode) != 3 or
                 city_iatacode == "EMPTY"
            )
            if conditions:
                return None
            url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

            headers = {
                "Authorization": self.token
            }

            parameters = {
                "originLocationCode": "LON",
                "destinationLocationCode": city_iatacode,
                "departureDate": date,
                "adults": 1,
            }
            try:
                self.response = requests.get(url=url, headers=headers, params=parameters, timeout=10)
            except requests.RequestException:
                continue
            except requests.exceptions.Timeout:
                continue
            self.prices = self.response.json()

            if self.generate_token_when_error(self.prices, self.response.status_code):       
                self.response = requests.get(url=url, params=parameters, headers=headers)
                self.prices = self.response.json()

            if "data" not in self.prices or len(self.prices["data"]) == 0:
                continue

            price = float(self.prices["data"][0]["price"]["grandTotal"])
            if self.cheapest_price is None or price < self.cheapest_price:
                self.cheapest_price = price
                self.cheapest_date = date
        return self.cheapest_price, self.cheapest_date
    
    def generate_token_when_error(self, response, status_code):
        if "error" in response or status_code == 401 or "errors" in response:
            new_token = self.get_new_token()
            self.token = f"Bearer {new_token['access_token']}"
            os.environ["amadeus_access_token"] = self.token
            return True
        return False
        