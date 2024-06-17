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
    allowed_values = ["off", "low", "medium", "max", "increase", "decrease"]

    scenarios = [
        build_scenario("Increase the fan please", "increase"),
        build_scenario("Decrease fan speed", "decrease"),
        build_scenario("Turn off fan", "off"),
        build_scenario("Set fan to full", "max"),
        build_scenario("Full fan please", "max"),
        build_scenario("Turn the fan up", "increase"),
        build_scenario("Turn the fan down", "decrease"),
        build_scenario("Set fan to low", "low"),
        build_scenario("Set fan to medium", "medium"),
        build_scenario("Set fan to maximum", "max"),
    ]

    def get_name(self):
        return "fan_control"

    def get_definition(self):
        return  {
            "name": self.get_name(),
            "description": "Set fan level",
            "parameters": [
                {
                    "name": "level",
                    "type": "string",
                    "allowed_values":  self.allowed_values
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"level":"' + select(self.allowed_values, name="level") + '"}'

        return { "level": llm["level"] }
    
    def build_random_scenario(self):
        return random.choice(self.scenarios)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "level" in parameters 
