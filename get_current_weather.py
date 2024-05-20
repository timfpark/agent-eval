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
        "Berlin", 
        "Fort Wayne", 
        "Indianapolis", 
        "Columbus", 
        "Charlotte", 
        "Detroit"
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
