import random
from guidance import select 

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
            "description": "Set audio system volume",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Audio level action",
                    }
                }
            },
        }
    
    def generate_parameters(self, llm):
        action_strings = ["increase", "decrease", "mute"]

        llm = llm + '{"action":"' + select(action_strings, name="action") + '"}'

        return { "action": llm["action"] }
    
    def build_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "change" in parameters 
