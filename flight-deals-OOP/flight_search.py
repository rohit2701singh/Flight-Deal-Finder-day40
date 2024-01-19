import requests


class FlightSearch:
    def __init__(self, tequila_api_key):
        """This class is responsible for talking to the Flight Search API."""

        self.__TEQUILA_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
        self.__tequila_location_endpoint = "https://api.tequila.kiwi.com/locations/query"
        self.__tequila_key = tequila_api_key

        self.__city = None
        self.__CURRENT_PLACE_NAME = None
        self.__CURRENT_PLACE_CODE = None
        self.__FINAL_DESTINATION = None
        self.__FLIGHT_PRICE = None
        self.__CURRENCY = None
        self.__CABIN = None
        self.__SEARCH_FROM_DATE = None
        self.__SEARCH_FINAL_DATE = None
        self.__limit_flights = None

        self.__tequila_header = {
            "apikey": self.__tequila_key,
            "Content-Type": "application/json"
        }

    def get_destination_code(self, city_name):
        """returns iata code of a city"""

        self.__city = city_name

        tequila_query = {
            "term": f"{self.__city}",
            "location_types": "city",
        }

        location_response = requests.get(url=self.__tequila_location_endpoint, params=tequila_query, headers=self.__tequila_header)
        location_response.raise_for_status()
        city_code = location_response.json()["locations"][0]["code"]
        return city_code
        # print(city, city_code)

    def check_flights(self, current_place, current_city_code, city_to_travel, search_from_date, search_end_date, price, currency, cabin="M", limit_flights=10):
        """returns a list of different flight details."""

        self.__CURRENT_PLACE_NAME = current_place
        self.__CURRENT_PLACE_CODE = current_city_code
        self.__FINAL_DESTINATION = city_to_travel
        self.__CURRENCY = currency
        self.__FLIGHT_PRICE = price
        self.__CABIN = cabin
        self.__SEARCH_FROM_DATE = search_from_date
        self.__SEARCH_FINAL_DATE = search_end_date
        self.__limit_flights = limit_flights

        tequila_search_query = {
            "fly_from": self.__CURRENT_PLACE_CODE,
            "fly_to": self.__FINAL_DESTINATION,
            "date_from": self.__SEARCH_FROM_DATE.strftime("%d/%m/%Y"),
            "date_to": self.__SEARCH_FINAL_DATE.strftime("%d/%m/%Y"),
            "price_to": self.__FLIGHT_PRICE,
            "curr": self.__CURRENCY,
            "limit": self.__limit_flights,
            "selected_cabins": self.__CABIN     # M (economy), W (economy premium), C (business), F (first class)
        }

        tequila_response = requests.get(url=self.__TEQUILA_SEARCH_ENDPOINT, params=tequila_search_query, headers=self.__tequila_header)
        tequila_data = tequila_response.json()
        print(tequila_data)
        data = tequila_data['data']

        content_data = {}
        i = 1
        for item in data:
            original_city = item["cityFrom"]
            original_city_code = item["flyFrom"]
            destination_city = item["cityTo"]
            destination_city_code = item["cityCodeTo"]
            airline = item["route"][0]["airline"]
            flight_num = item["route"][0]["flight_no"]
            departure_date = item["local_departure"].split("T")[0]

            flight_price = item["price"]
            eur_price = item["conversion"]["EUR"]

            content_data[f"flight{i}"] = {
                f"{original_city}({original_city_code}) to {destination_city}({destination_city_code}":
                    {
                        "airlines": airline,
                        "flight num": flight_num,
                        'departure date': departure_date,
                        "price": f"INR{flight_price}(EUR {eur_price})"
                    }
            }

            i += 1
        return content_data