# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager(
    authorization_key="Bearer rxxxxxxxccxcfff22gh",
    sheet_get_endpoint="https://api.sheety.co/4xxxxxxcvvvcxxcxxxc8xxx1a/flightDeal/prices",
    sheet_put_endpoint="https://api.sheety.co/xxxxxxxxxxxxxxxxxxcvcx1a/flightDeal/prices"
)

flight_search = FlightSearch(tequila_api_key="mkxxxxxxxsczdxscxxxxxxxxxxdX4")

# ----------fill iata code in google sheet---------

sheet_data = data_manager.get_destination_data()
for city_iata_data in sheet_data:
    for (city_name, iata_code) in city_iata_data.items():
        if city_iata_data[city_name] == "":
            city_iata_data[city_name] = flight_search.get_destination_code(city_name)
            print(city_name, city_iata_data[city_name])
data_manager.update_destination_codes(sheet_with_iata=sheet_data)

# ----------- get user set flight price ----------

user_set_flight_price = data_manager.get_price_info()
print(user_set_flight_price)

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# --------get flights and send mail----------

message_draft = []
for destination_and_price in user_set_flight_price:
    for (code, price) in destination_and_price.items():

        flight = flight_search.check_flights(
            current_place="Mumbai",
            current_city_code="BOM",
            city_to_travel=code,
            search_from_date=tomorrow,
            search_end_date=six_month_from_today,
            price=destination_and_price[code],
            cabin="M",
            currency="INR",
            limit_flights=5,
        )
        message_draft.append(flight)
# print(message_draft)
message = NotificationManager(message_draft)






