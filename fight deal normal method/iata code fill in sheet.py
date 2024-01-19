import requests

tequila_location_endpoint = "https://api.tequila.kiwi.com/locations/query"
sheety_get_endpoint = "https://api.sheety.co/6xxxxxxxxxxxxxxxx81a/flightDeal/prices"
sheety_put_endpoint = "https://api.sheety.co/4xx62cccccxxxcccccc/flightDeal/prices"

# --------------get data from sheet and create a city list to search for IATA code----------------

sheety_header = {
    "Authorization": "Bearer roxxxxx1sxxxxg",
    "Content-Type": "application/json"
}

get_sheety_response = requests.get(url=sheety_get_endpoint, headers=sheety_header)
sheety_response_data = get_sheety_response.json()["prices"]
# print(sheety_response_data)

city_list = [item["city"] for item in sheety_response_data]

# -------------- get IATA code using tequila api and enter in sheet----------------------

tequila_header = {
    "apikey": "mkxcxxcxxxcxcxxccxhxxX4",
    "Content-Type": "application/json"
}

row = 2
for city in city_list:
    tequila_query = {
        "term": f"{city}",
        "location_types": "city",
    }
    location_response = requests.get(url=tequila_location_endpoint, params=tequila_query, headers=tequila_header)
    location_response.raise_for_status()
    city_code = location_response.json()["locations"][0]["code"]
    print(city, city_code)

    iata_entry = {
        "price": {
            "iataCode": city_code
        }
    }

    iata_code_fill = requests.put(url=f"{sheety_put_endpoint}/{row}", json=iata_entry, headers=sheety_header)
    row += 1


















