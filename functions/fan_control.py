import random

class FanControl:

    scenarios = [
        {
            "function": "fan_control",
            "user_input": "Increase the fan",
            "expected": {
                "function": "fan_control",
                "arguments": {
                    "action": "increase",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Decrease fan speed",
            "expected": {
                "function": "fan_control",
                "arguments": {
                    "action": "decrease",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Turn off fan",
            "expected": {
                "function": "fan_control",
                "arguments": {
                    "action": "off",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Turn the fan up a bit",
            "expected": {
                "function": "fan_control",
                "arguments": {
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
            },
        }
    
    def generate_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "action" in arguments 
