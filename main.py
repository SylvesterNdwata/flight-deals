from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
import json
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification = NotificationManager()

sheet_data = data_manager.get_sheet_data()
user_emails = data_manager.get_customer_emails()
    
for row in sheet_data:
    city = row["city"]
    iatacode = flight_search.get_iata_code(city)
    row["iataCode"] = iatacode
    id = row["id"]
    price = flight_search.get_cheap_flights(city_iatacode=iatacode)
    print(f"Getting flights for {city}...")
    pprint(f"{city}: {price}")
    new_price = price[0] if price else None
    date = price[1] if price else None
    if new_price is not None and new_price < float(row["lowestPrice"]):
        data_manager.update_flight_price(price=new_price, id=id)
        notification.send_message(price=new_price, date=date, to_city=iatacode)
        for email in user_emails:
            notification.send_email(email=email, price=new_price, to_city=iatacode, date=date)
        

#     # data_manager.update_iata_codes(iatacode=row["iataCode"], id=id)

# print(sheet_data)

# for row in sheet_data:
#     city = row["city"]
#     iatacode = flight_search.get_iata_code(city)
#     row["iataCode"] = iatacode
#     price = flight_search.get_cheap_flights(city_iatacode=iatacode)
#     print(price)

# all_prices = {}
# for row in sheet_data:
#     iatacode = row["iataCode"]
#     price = flight_search.get_cheap_flights(city_iatacode=iatacode)
#     all_prices[iatacode] = price
    
# with open("prices.json", "w", encoding="utf-8") as f:
#         json.dump(all_prices, f, indent=4)


print(user_emails)

    