import requests
import os
# This class is responsible for talking to the Google Sheet.


class DataManager:

    def __init__(self):
        self.data = {}
        self.current_endpoint = ""

    def update_google_sheet(self):
        response = requests.put(url=self.current_endpoint, headers=sheety_headers, json=self.data)
        response.raise_for_status()
        return

    def update_sheet(self, data):
        for num in range(len(data)):
            self.data = {
                "price": {
                    "city": data[num]["city"],
                    "iataCode": data[num]["iataCode"],
                    "lowestPrice": data[num]["lowestPrice"],
                }
            }
            self.current_endpoint = f"{SHEETY_ENPOINT}/{data[num]['id']}"
            self.update_google_sheet()

    def initial_data(self):
        response = requests.get(url=SHEETY_ENPOINT, headers=sheety_headers)
        response.raise_for_status()
        data = response.json()
        sheet_data = data["prices"]
        return sheet_data


SHEETY_ENPOINT = "https://api.sheety.co/01d994fc556980e962983f4d4e778998/myFlightDeals/prices"
env_bear_token = os.environ["BEARER_TOK_ENV"]
bearer_token = env_bear_token
sheety_headers = {
    "Authorization": f"Bearer {bearer_token}",
}
