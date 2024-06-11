import random
from guidance import select 

def build_scenario(user_input, volume):
    return {
        "function": "volume_control",
        "user_input": user_input,
        "expected": {
            "function": "volume_control",
            "parameters": {
                "volume": volume,
            }
        }
    }

class VolumeControl:
    allowed_volume_values =  ["increase", "decrease", "mute", "15", "30", "45"]

    scenarios = [
        build_scenario("Set volume to 45", "45"),
        build_scenario("Increase volume please", "increase"),
        build_scenario("Set volume to 30", "30"),
        build_scenario("Decrease volume", "decrease"),
        build_scenario("Please lower the volume", "decrease"),
        build_scenario("Mute audio", "mute"),
        build_scenario("Please turn up the volume", "increase"),
        build_scenario("Set volume to 15", "15"),
    ]

    def get_name(self):
        return "volume_control"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Set audio volume",
            "parameters": [
                {
                    "name": "volume",
                    "type": "string",
                    "allowed_values": self.allowed_volume_values
                }
            ]
        }

    def generate_parameters(self, llm):
        llm = llm + '{"volume":"' + select(self.allowed_volume_values, name="volume") + '"}'

        return { "volume": llm["volume"] }
    
    def build_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "volume" in parameters 
