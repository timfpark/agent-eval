import random

class GetCarTemperatureSetpoint:
    templates = [
        "What is the temperature currently set to?",
        "What is the temperature set to?",
        "What is the current car temperature?"
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
        "Do you know what temperature it’s set at?",
        "Can you tell me how warm or cool it is set?",
        "What’s the thermostat set to?",
        "Can you tell me the current temp?"
    ]   

    def get_name(self):
        return "get_car_temperature_setpoint"

    def get_definition(self):
        return {    
            "name": self.get_name(),
            "description": "Get the current set point temperature for the vehicle's interior",
            "parameters": [],
            "required": [],
            "returns": [
                {
                    "name": "temperature",
                    "type": "float",
                }
            ]
        }
    
    def generate_scenario(self, template):
        return {
            "function": self.get_name(),
            "user_input": template,
            "expected": {
                "function": self.get_name(),
                "arguments": {}
            }
        } 

    def generate_random_scenario(self):
        template = random.choice(self.templates)

        return self.generate_scenario(template)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and len(arguments) == 0