# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


# from rasa_sdk.events import SlotSet
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

class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "action_check_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("In the Action Check Weather")
        dispatcher.utter_message("Hello World! from custom action")

        return []


class ActionSearchRestaurant(Action):

    def name(self) -> Text:
        return "action_search_restaurant"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message["entities"]
        print(entities)
        print(type(entities))
        for e in entities:
            if e["entity"] == "hotel":
                name = e["value"]

            if name == "indian":
                message = "Indian 1 ,Indian 2 ,Indian 3 ,Indian 4"
            if name == "chinese":
                message = "chinese 1 ,chinese 2 ,chinese 3 ,chinese 4"

            if name == "":
                message = "Bot could not understand your input"
        print("The message value is", message)
        dispatcher.utter_message(text=message)

        return []


class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = requests.get("https://api.covid19india.org/data.json").json()
        entities = tracker.latest_message["entities"]
        print("Latest message is ", entities)
        state = ""

        for e in entities:
            if e["entity"] == "state":
                state = e["value"]
            # print("The message value is", message)
            dispatcher.utter_message(text="Hello World!" + state)

        message ="Please enter correct state name"

        if state == "india":
            state = "Total"

        for data in response["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = ("Active:" + data["active"] +" "+ "Confirmed:" + data["confirmed"] +
                   " " + "recovered:" + data["recovered"]+ " " + "Deaths:" + data["deaths"]
                   )
        dispatcher.utter_message(text=message)

        return []
