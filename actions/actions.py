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
price = best_flight['price']
airline = best_flight['flights'][0]['airline']
departure = best_flight['flights'][0]['departure_airport']['name']
arrival  = best_flight['flights'][0]['arrival_airport']['name']
out_date = best_flight['flights'][0]['arrival_airport']['time']
return_date = best_flight['flights'][0]['departure_airport']['time']


print(best_flight)











class ActionGetFlight(Action):
    def name(self) -> Text:
        return 'action_get_flight'
    
    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        departure_id = tracker.get_slot("departure_id")
        arrival_id = tracker.get_slot("arrival_id")
        outbound_date = tracker.get_slot("outbound_date")
        return_date = tracker.get_slot("return_date")

        if not departure_id or not arrival_id or not outbound_date:
            dispatcher.utter_message(text="Please provide complete flight details.")
            return []


        base_url = 'https://serpapi.com/search.json?engine=google_flights&departure_id=PEK&arrival_id=AUS&outbound_date=2024-11-30&return_date=2024-12-06&currency=USD&hl=en'
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD",
            "hl": "en",
            "api_key": "f506b14c2ebeac4812c4ea82d326474cd9a7de1726ddc7f47ce2db901d7c474e"
                }
        try:
            # Perform the API search
            search = GoogleSearch(params)
            results = search.get_dict()

            # Extract flight information
            best_flight = results['best_flights'][0]
            if "best_flights" not in results or not results["best_flights"]:
                dispatcher.utter_message(text="No flights found for your criteria.")
                return []

            # Extract details from the first flight
            airline = best_flight['flights'][0]['airline']
            price = best_flight['price']
            departure_time = best_flight['flights'][0]['arrival_airport']['time']
            arrival_time = best_flight['flights'][0]['arrival_airport']['name']

            # Format and send the response
            message = (
                f"Flight found:\n"
                f"Airline: {airline}\n"
                f"Price: {price}\n"
                f"Departure: {departure_time}\n"
                f"Arrival: {arrival_time}"
            )
            dispatcher.utter_message(text=results)

        except Exception as e:
            # Handle errors gracefully
            dispatcher.utter_message(text=f"Failed to fetch flight details: {e}")

        return []