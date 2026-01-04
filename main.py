import requests
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
import os
from dotenv import load_dotenv

load_dotenv()

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_sheet_data()

    
for row in sheet_data:
    city = row["city"]
    iatacode = flight_search.get_iata_code(city)
    row["iataCode"] = iatacode
    id = row["id"]
    data_manager.update_iata_codes(iatacode=row["iataCode"], id=id)

print(sheet_data)