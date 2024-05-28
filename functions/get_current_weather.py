import random

class GetCurrentWeatherTool:
    city_names = [
        "Singapore", 
        "London", 
        "San Francisco", 
        "New York", 
        "Los Angeles", 
        "Chicago", 
        "Houston", 
        "Phoenix", 
        "Philadelphia", 
        "San Antonio", 
        "Fort Wayne", 
        "Indianapolis", 
        "Columbus", 
        "Charlotte", 
        "Detroit",
        "Boston",
        "Memphis",
        "Seattle",
        "Denver",
        "Washington D.C.",
        "Nashville",
        "Baltimore",
        "Louisville",
        "Madrid",
        "Barcelona",
        "Valencia",
        "Seville",
        "Zaragoza",
        "Málaga",
        "Zurich",
        "Geneva",
        "Basel",
        "Lausanne",
        "Bern",
        "Winterthur",
        "Lucerne",
        "St. Gallen",
        "Lugano",
        "Rome",
        "Milan",
        "Naples",
        "Turin",
        "Palermo",
        "Paris",
        "Marseille",
        "Lyon",
        "Toulouse",
        "Nice",
        "Nantes",
        "Strasbourg",
        "Montpellier",
        "Bordeaux",
        "Lille",
        "Dublin",
        "Cork",
        "Galway",
        "Belfast",
        "Derry",
        "Lisbon",
        "Porto",
        "Braga",
        "Faro",
        "Coimbra",
        "Funchal",
        "Ponta Delgada",
        "Berlin",
        "Hamburg",
        "Munich",
        "Cologne",
        "Frankfurt",
        "Stuttgart",
        "Düsseldorf",
        "Dortmund",
        "Essen",
        "Leipzig",
        "Dresden",
        "Hanover",
        "Nuremberg",
        "Sydney",
        "Melbourne",
        "Brisbane",
        "Perth",
        "Auckland",
        "Soquel",
        "Santa Cruz",
        "Davenport",
        "Capitola",
        "Aptos",
        "Watsonville",
        "Scotts Valley",
        "Felton",
        "Boulder Creek",
        "Ben Lomond",
        "Morgan Hill",
        "Gilroy",
        "San Martin",
        "Los Gatos",
        "Saratoga",
        "Cupertino",
        "Sunnyvale",
        "Sargent",
        "Aromas",
        "San Juan Bautista",
        "Hollister",
        "Tres Pinos",
        "Prunedale"
    ]

    templates = [
        "What is the weather like in {}?", 
        "What is the temperature in {}?", 
        "How warm is it in {}?"
    ]

    def get_name(self):
        return "get_current_weather"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city to retrieve weather",
                    },
                },
                "required": ["location"],
            },
        }
    
    def generate_scenario(self):
        city_name = random.choice(self.city_names)
        template = random.choice(self.templates)
        return {
            "tool_name": self.get_name(),
            "prompt": template.format(city_name),
            "expected_arguments": {
                "location": city_name,
            }
        }
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "location" in arguments

