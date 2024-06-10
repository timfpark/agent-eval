import random
from guidance import select 

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
            "user_input": "Set fan to max",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "max",
                }
            }
        },
        {
            "function": "fan_control",
            "user_input": "Set fan to full",
            "expected": {
                "function": "fan_control",
                "parameters": {
                    "action": "max",
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
            "description": "Set fan level",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "description": "Desired fan level action",
                    }
                }
            }
        }
    
    def generate_parameters(self, llm):
        action_strings = ["off", "low", "medium", "max", "increase", "decrease"]

        llm = llm + '{"action":"' + select(action_strings, name="action") + '"}'

        return { "action": llm["action"] }
    
    def build_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "action" in parameters 
