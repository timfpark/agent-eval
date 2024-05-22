import random

class GetCarTemperatureSetpointTool:
    templates = [
        "What is the temperature currently set to?",
        "What is the temperature set to?",
        "What is the current car temperature?"
    ]

    def get_name(self):
        return "get_car_temperature_setpoint"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Get the current set point temperature for the car's cabin",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        }
    
    def generate_scenario(self):
        template = random.choice(self.templates)

        return {
            "tool_name": self.get_name(),
            "prompt": template,
            "expected_arguments": {}
        }
