import requests


class DataManager:
    def __init__(self, authorization_key, sheet_get_endpoint, sheet_put_endpoint):
        """This class is responsible for talking to the Google Sheet,
        takes input for authorization and initialization purpose."""

        self.__city_list = None
        self.__updated_data = None

        self.__sheety_get_endpoint = sheet_get_endpoint
        self.__sheety_put_endpoint = sheet_put_endpoint
        self.__authorization = authorization_key

        self.__sheety_header = {
            "Authorization": self.__authorization,
            "Content-Type": "application/json"
        }

        self.__get_sheety_response = requests.get(url=self.__sheety_get_endpoint, headers=self.__sheety_header)
        # print(self.__get_sheety_response.json())

    def get_destination_data(self):
        """get data from Google sheet and return a list with nested dictionary.
        dictionary contains city_name and blank iata_code."""

        self.__city_list = []
        sheety_response_data = self.__get_sheety_response.json()["prices"]
        # print(sheety_response_data)    # [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 20000, 'id': 2},.......]

        self.__city_list = [{item["city"]: item["iataCode"]} for item in sheety_response_data]

        return self.__city_list  # [{'Paris': ''}, {'Berlin': 'BER'}, {'Tokyo': ''}] if iata code is empty

    def update_destination_codes(self, sheet_with_iata):
        """take a list as input which contains nested dictionary. fill iata code into the sheet."""

        self.__updated_data = sheet_with_iata

        row = 2
        for city in self.__updated_data:
            for (city_name, code) in city.items():
                iata_entry = {
                    "price": {
                        "iataCode": city[city_name]
                    }
                }

                iata_code_fill = requests.put(url=f"{self.__sheety_put_endpoint}/{row}", json=iata_entry, headers=self.__sheety_header)
                # print(iata_code_fill.json())
                row += 1

    def get_price_info(self):
        """get price details from sheet. and return a list."""

        sheety_response_data = self.__get_sheety_response.json()["prices"]
        city_price_list = [{item["iataCode"]: item["lowestPrice"]} for item in sheety_response_data]

        # print(self.__get_sheety_response.json())
        # print(city_price_list)  # [{'PAR': 25000}, {'BER': 30000}, {'TYO': 15000}]

        return city_price_list
