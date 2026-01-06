from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager

data_manager = DataManager()
flight_search = FlightSearch()

sheet_data = data_manager.get_sheet_data()

    
for row in sheet_data:
    city = row["city"]
    iatacode = flight_search.get_iata_code(city)
    row["iataCode"] = iatacode
    id = row["id"]
    price = flight_search.get_cheap_flights(city_iatacode=iatacode)
    print(f"Getting flights for {city}...")
    print(f"{city}: {price}")
    # data_manager.update_iata_codes(iatacode=row["iataCode"], id=id)

# print(sheet_data)

# for row in sheet_data:
#     city = row["city"]
#     iatacode = flight_search.get_iata_code(city)
#     row["iataCode"] = iatacode
#     print(iatacode)

