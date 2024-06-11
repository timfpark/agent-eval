from guidance import select 
import random

def build_scenario(user_input, level):
    return {
        "function": "fan_control",
        "user_input": user_input,
        "expected": {
            "function": "fan_control",
            "parameters": {
                "level": level,
            }
        }
    }

class FanControl:
    scenarios = [
        build_scenario("Increase the fan please", "increase"),
        build_scenario("Decrease fan speed", "decrease"),
        build_scenario("Turn off fan", "off"),
        build_scenario("Set fan to full", "max"),
        build_scenario("Full fan please", "max"),
        build_scenario("Turn the fan up", "increase"),
    ]

    def get_name(self):
        return "fan_control"

    def get_definition(self):
        return  {
            "name": self.get_name(),
            "description": "Set fan level",
            "parameters": { 
                "level": "new fan level or action"
            }
        }
    
    def generate_parameters(self, llm):
        action_strings = ["off", "low", "medium", "max", "increase", "decrease"]

        llm = llm + '{"level":"' + select(action_strings, name="level") + '"}'

        return { "level": llm["level"] }
    
    def build_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "level" in parameters 
