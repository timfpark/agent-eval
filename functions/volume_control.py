import random

class VolumeControl:

    scenarios = [
        {
            "function": "volume_control",
            "user_input": "Increase volume",
            "expected": {
                "function": "volume_control",
                "parameters": {
                    "action": "increase",
                }
            }
        },
        {
            "function": "volume_control",
            "user_input": "Decrease volume",
            "expected": {
                "function": "volume_control",
                "parameters": {
                    "action": "decrease",
                }
            }
        },
        {
            "function": "volume_control",
            "user_input": "Mute audio",
            "expected": {
                "function": "volume_control",
                "parameters": {
                    "action": "mute",
                }
            }
        }
    ]

    def get_name(self):
        return "volume_control"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Control the volume of the car's audio system",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "The desired audio level action",
                    }
                },
                "required": ["action"],
                "returns": []
            },
        }
    
    def generate_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "change" in parameters 
