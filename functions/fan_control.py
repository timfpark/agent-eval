import random

class FanControl:

    scenarios = [
        {
            "function": "fan_control",
            "user_input": "Increase the fan",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "increase",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Decrease fan speed",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "decrease",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Turn off fan",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "off",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Turn the fan up a bit",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "increase",
                }
            }
        }
    ]

    def get_name(self):
        return "fan_control"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Control the fan level of the main heating and cooling system",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The desired fan level action",
                    }
                },
                "required": ["action"],
                "returns": []
            },
        }
    
    def generate_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "action" in parameters 
