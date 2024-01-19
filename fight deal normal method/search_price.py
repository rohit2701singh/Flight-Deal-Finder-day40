import requests
import os
from twilio.rest import Client

SHEETY_GET_ENDPOINT = "https://api.sheety.co/4xxxxxxxxccxccxcxcxx1a/flightDeal/prices"
TEQUILA_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
CURRENT_PLACE_NAME = "india"
CURRENT_PLACE_CODE = "DEL"
CURRENCY = "INR"
CABIN = "M"
SEARCH_FROM_DATE = "20/1/2024"
SEARCH_FINAL_DATE = "30/1/2024"    # type set to string

account_sid = os.environ.get("ACCOUNT_SID_TWILIO")
auth_token = os.environ.get("AUTH_TOKEN_TWILIO")

sheety_header = {
    "Authorization": "Bearer roxxxxccxhixxxxgh",
    "Content-Type": "application/json"
}

get_sheety_response = requests.get(url=SHEETY_GET_ENDPOINT, headers=sheety_header)
sheety_response_data = get_sheety_response.json()["prices"]
print(get_sheety_response.json())

city_price_list = [{item["iataCode"]: item["lowestPrice"]} for item in sheety_response_data]
print(city_price_list)  # [{'PAR': 25000}, {'BER': 30000}, {'TYO': 15000}]

tequila_header = {
    "apikey": "mkxxxxcxcxcxcxccxcxccxxx4",
    "Content-Type": "application/json"
}

message_draft = []
for city_price in city_price_list:  # {'PAR': 25000}
    for (city, price) in city_price.items():
        tequila_search_query = {
            "fly_from": CURRENT_PLACE_CODE,
            "fly_to": city,
            "date_from": SEARCH_FROM_DATE,
            "date_to": SEARCH_FINAL_DATE,
            "price_to": price,
            "curr": CURRENCY,
            "limit": 5,
            # "selected_cabins": CABIN     # M (economy), W (economy premium), C (business), F (first class).
        }

        tequila_response = requests.get(url=TEQUILA_SEARCH_ENDPOINT, params=tequila_search_query, headers=tequila_header)
        data = tequila_response.json()
        flight_data = data["data"]

        for item in flight_data:
            departure_date = item["local_departure"].split("T")[0]
            city_to_name = item["cityTo"]
            flight_price = item["price"]
            price_convert_eur = item["conversion"]["EUR"]
            message_draft.append(f"from: {CURRENT_PLACE_NAME}-({CURRENT_PLACE_CODE}), to: {city_to_name}-({city}), departure date: {departure_date} and fare: ₹{flight_price} (€{price_convert_eur})")
print(message_draft)

if len(message_draft) != 0:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                         body=f"flight detail: {message_draft}",
                         from_='+12cccxxxxxx96',
                         to='+91xxxxxx09'
                     )
    print(message.status)
