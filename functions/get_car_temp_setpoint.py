import random
from guidance import gen 

class GetCarTemperatureSetpoint:
    templates = [
        "What is the temperature currently set to?",
        "What is the temperature set to?",
        "What is the current car temperature?",
        "At what temperature is it currently set?",
        "Can you tell me the current temperature setting?",
        "What temperature is it set to right now?",
        "Could you let me know the present temperature setting?",
        "What's the current temperature setting?",
        "Can you provide the current temperature setting?",
        "How hot or cold is it set to?",
        "What's the temperature set to right now?",
        "Can you check the current temperature for me?",
        "Can you tell me the current temperature?",
        "Do you know what temperature the car is set to?",
        "Can you tell me how warm or cool it is set?",
        "What’s the thermostat set to?",
        "Can you tell me the current temp?"
    ]   

    def get_name(self):
        return "get_car_temperature_setpoint"

    def get_definition(self):
        return {    
            "name": self.get_name(),
            "description": "Get the current set point temperature",
            "parameters": {},
        }
    
    def generate_parameters(self, _llm):
        return {}

    def build_scenario(self, template):
        return {
            "function": self.get_name(),
            "user_input": template,
            "expected": {
                "function": self.get_name(),
                "parameters": {}
            }
        } 

    def build_random_scenario(self):
        template = random.choice(self.templates)

        return self.build_scenario(template)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and len(parameters) == 0