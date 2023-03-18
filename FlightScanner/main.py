from data_manager import DataManager
from flight_search import FlightSearch

data_manager = DataManager()
flight_search = FlightSearch()
data = data_manager.initial_data()

ORIGIN_CITY_IATA = "PER"

for num in range(len(data)):
    if data[num]["iataCode"] == "":
        code = flight_search.code_search(data[num]["city"])
        data[num]["iataCode"] = code

data_manager.update_sheet(data)


for destination in data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        )
