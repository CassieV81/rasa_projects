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
import random
from string import capwords

class ActionCheckWeather(Action):

    def name(self) -> Text:
        return "action_check_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # I realise it might not have been necessary to try catch invalid inputs
        # since the bot will select valid inputs through entities selection
        try:
            location = tracker.get_slot("location")
            
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=67cb3adbca2571ac10da532e66620b73")

            response.raise_for_status()
            
            weather = response.json()["main"]["temp"]

            def convert_K_to_C(num):
                return int(num - 273.15)
            
            weather_C = convert_K_to_C(weather)

            dispatcher.utter_message(text=f"The weather in {location} is {weather_C}°C")
        except requests.exceptions.RequestException:
            dispatcher.utter_message(text="Your input is invalid")
            
        return []
    
class ActionPlayRPS(Action):

    def name(self) -> Text:
        return "action_play_RPS"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        player = capwords(tracker.get_slot("choices"))
        bot = capwords(random.choice(['rock', 'paper', 'scissors']))

        if player == bot:
            dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. It's a Tie!")
        elif player == 'Rock':
            if bot == 'Scissors':
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {player} crushes {bot}, You Win!")
            else:
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {bot} cover {player}, You Lose!")
        elif player == 'Scissors':
            if bot == 'Paper':
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {player} cuts {bot}, You Win!")
            else:
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {bot} crushes {player}, You Lose!")
        elif player == 'Paper':
            if bot == 'Rock':
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {player} covers {bot}, You Win!")
            else:
                dispatcher.utter_message(text=f"You chose {player} and I chose {bot}. {bot} cuts {player}, You Lose!")

        return[]
