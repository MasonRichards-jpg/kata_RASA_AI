from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from serpapi import GoogleSearch
from rasa_sdk.events import SlotSet
from apikey import apikeyy

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
        
        print("Departure ID:", departure_id)
        print("Arrival ID:", arrival_id)
        print("Outbound Date:", outbound_date)
        print("Return Date:", return_date)

        def process_date_entity(date_entity):
            if isinstance(date_entity, dict) and 'value' in date_entity:
                return date_entity['value'][:10]  
            return date_entity

        outbound_date = process_date_entity(outbound_date)
        return_date = process_date_entity(return_date)

        if not departure_id or not arrival_id or not outbound_date:
            dispatcher.utter_message(text="Please provide complete flight details.")
            return []
        
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "USD",
            "hl": "en",
            "api_key": apikeyy
        }
        print("API Parameters:", params)

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            print("API Response:", results)

            if "best_flights" not in results or not results["best_flights"]:
                dispatcher.utter_message(text="No flights found for your criteria.")
                return []

            best_flight = results['best_flights'][0]
            airline = best_flight['flights'][0]['airline']
            price = best_flight['price']
            departure_time = best_flight['flights'][0]['departure_airport']['time']
            arrival_time = best_flight['flights'][0]['arrival_airport']['time']

            message = (
                f"Flight found:\n"
                f"Airline: {airline}\n"
                f"Price: {price}\n"
                f"Departure Time: {departure_time}\n"
                f"Arrival Time: {arrival_time}"
            )
            dispatcher.utter_message(text=message)

        except Exception as e:
            dispatcher.utter_message(text=f"Failed to fetch flight details: {e}")

        return []
