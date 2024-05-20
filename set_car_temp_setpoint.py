import random

class SetCarTemperatureSetpointTool:
    temperatures = [
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75
    ]

    templates = [
        "Set the temperature to {} degrees please",
        "Please set the temperature to {}",
        "Could you adjust the thermostat to {} degrees, please?"
    ]

    def get_name(self):
        return "set_car_temperature_setpoint"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Set temperature of car's cabin",
            "parameters": {
                "type": "object",
                "properties": {
                    "temperature": {
                        "type": "number",
                        "description": "The desired temperature set point for the car's cabin",
                    }
                },
                "required": ["temperature"],
            },
        }
    
    def generate_scenario(self):
        temperature = random.choice(self.temperatures)
        template = random.choice(self.templates)
        return {
            "tool_name": self.get_name(),
            "prompt": template.format(temperature),
            "expected_arguments": {
                "temperature": temperature,
            }
        }
