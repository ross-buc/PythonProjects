import requests
from datetime import datetime as dt
from dateutil.relativedelta import *
from flight_data import FlightData
from notification_manager import NotificationManager
import os

notification_manager = NotificationManager()
time_now = dt.now()
date_now_format = time_now.strftime("%d/%m/%Y")
six_months = time_now.date() + relativedelta(months=+6)
six_months_format = six_months.strftime("%d/%m/%Y")
env_kiwi_api = os.environ.get("KIWI_API_ENV")
KIWI_API = env_kiwi_api
KIWI_ENDPOINT = "https://api.tequila.kiwi.com/locations/query"
KIWI_SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
FLIGHT_FROM = "PER"
FLIGHT_TO = "MEL"

booking_header = {
    "apikey": KIWI_API,
}


class FlightSearch:

    def __init__(self):
        pass

    def code_search(self, code):
        location_params = {"term": code}
        response = requests.get(url=KIWI_ENDPOINT, headers=booking_header, params=location_params)
        response.raise_for_status()
        data = response.json()
        iata_code = data["locations"][0]["code"]
        return iata_code

    def check_flights(self, origin_city_code, destination_city_code):
        headers = {"apikey": KIWI_API}
        booking_params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": date_now_format,
            "date_to": six_months_format,
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "adults": 1,
            "curr": "AUD",
            "price_from": 1,
            "price_to": 420,
        }
        response = requests.get(url=KIWI_SEARCH_ENDPOINT, headers=headers, params=booking_params)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        notification_manager.alert_by_text(flight_data.price, flight_data.origin_city, flight_data.origin_airport,
                                           flight_data.destination_city, flight_data.destination_airport,
                                           flight_data.out_date, flight_data.return_date)
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data
