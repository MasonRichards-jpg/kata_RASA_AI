# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from serpapi import GoogleSearch
base_url = 'https://serpapi.com/search.json?engine=google_flights&departure_id=PEK&arrival_id=AUS&outbound_date=2024-11-30&return_date=2024-12-06&currency=USD&hl=en'
params = {
            "engine": "google_flights",
            "departure_id": "ORD",
            "arrival_id": "AUS",
            "outbound_date": "2024-11-30",
            "return_date": "2024-12-06",
            "currency": "USD",
            "hl": "en",
            "api_key": "f506b14c2ebeac4812c4ea82d326474cd9a7de1726ddc7f47ce2db901d7c474e"
                }
search = GoogleSearch(params)
results = search.get_dict()
best_flight = results['best_flights'][0]
print(best_flight['flights'][0]['departure_airport']['time'])


class ActionGetFlight(Action):
    def name(self) -> Text:
        return 'action_get_flight'
    
    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        base_url = 'https://serpapi.com/search.json?engine=google_flights&departure_id=PEK&arrival_id=AUS&outbound_date=2024-11-30&return_date=2024-12-06&currency=USD&hl=en'
        params = {
            "engine": "google_flights",
            "departure_id": "PEK",
            "arrival_id": "AUS",
            "outbound_date": "2024-11-30",
            "return_date": "2024-12-06",
            "currency": "USD",
            "hl": "en",
            "api_key": "f506b14c2ebeac4812c4ea82d326474cd9a7de1726ddc7f47ce2db901d7c474e"
                }
        search = GoogleSearch(params)
        try:
            results = search.get_dict()
        except Exception as e:
            dispatcher.utter_message(text=f"Failed to fetch flight details: {e}")
            return []

        
        
        
        

        best_flight = results['best_flights'][0]
        price = best_flight['price']
        airline = best_flight['flights'][0]['airline']
        departure = best_flight['flights'][0]['departure_airport']['name']
        arrival  = best_flight['flights'][0]['arrival_airport']['name']
        out_date = best_flight['flights'][0]['arrival_airport']['time']
        return_date = best_flight['flights'][0]['departure_airport']['time']
        message = (
            f"Here is the best flight I found:\n"
            f"Airline: {airline}\n"
            f"Price: {price}\n"
            f"Departure: {departure}\n"
            f"Arrival: {arrival}\n"
            f"Outbound Date: {out_date}\n"
            f"Return Date: {return_date}"
        )
        dispatcher.utter_message(text=message)
        return []