from guidance import select 
import random
import re

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
    allowed_volume_values = ["increase", "decrease", "mute", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    specific_volume_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    scenarios = [
        build_scenario("Please adjust the volume to {}", "{}"),
        build_scenario("Set the volume to {}", "{}"),
        build_scenario("Can you set the volume to {}", "{}"),
        build_scenario("Adjust the volume setting to {}", "{}"),
        build_scenario("Set the audio to {}", "{}"),
        build_scenario("Please turn the volume to {}", "{}"),

        build_scenario("Increase volume please", "increase"),
        build_scenario("Decrease volume", "decrease"),
        build_scenario("Please lower the volume", "decrease"),
        build_scenario("Mute audio", "mute"),
        build_scenario("Please turn up the volume", "increase"),
        build_scenario("Please make it louder", "increase"),
        build_scenario("Turn the volume up, please.", "increase"),
        build_scenario("Can you decrease the volume?", "decrease"),
        build_scenario("Mute audio", "mute"),
        build_scenario("Can you mute?", "mute"),
        build_scenario("Please mute", "mute"),
        build_scenario("Can you increase the volume?", "increase"),
        build_scenario("Can you turn it up?", "increase"),
        build_scenario("Can you make it louder?", "increase"),
        build_scenario("Can you turn it down?", "decrease"),
        build_scenario("Can you decrease the volume?", "decrease"),
        build_scenario("Can you lower the volume?", "decrease"),
    ]

    def get_name(self):
        return "volume_control"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Set specific value, increase, decrease, or mute audio volume",
            "parameters": [
                {
                    "name": "volume",
                    "type": "string",
                }
            ]
        }

    def generate_parameters(self, llm):
        llm = llm + '{"volume":"' + select(self.allowed_volume_values, name="volume") + '"}'

        return { "volume": llm["volume"] }
    
    def build_random_scenario(self):
        scenario = random.choice(self.scenarios)

        if bool(re.search(r'[{}]', scenario["user_input"])):
            volume = random.choice(self.specific_volume_values)
            
            scenario["user_input"] = scenario["user_input"].format(volume)
            scenario["expected"]["parameters"]["volume"] = volume

        return scenario
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "volume" in parameters 
