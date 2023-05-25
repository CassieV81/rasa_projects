# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_check_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = tracker.get_slot("location")
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=67cb3adbca2571ac10da532e66620b73")
        
        weather = response.json()["main"]["temp"]

        def convert_K_to_C(num):
             return int(num - 273.15)
        
        weather_C = convert_K_to_C(weather)

        dispatcher.utter_message(text=f"The weather in {location} is {weather_C}°C")

        return []
