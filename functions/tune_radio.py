import random

class TuneRadio:
    stations = [
        101.7, 90.3, 94.5, 102.3, 98.5, 99.1, 100.3, 97.9, 96.7, 103.1, "KQED", "The Beach", "BBC Radio 1", "KFOG", "KISS FM", "Radio Bob"
    ]

    templates = [
        "Can you tune the radio to {} please",
        "Change the radio to {}",
        "Please go to {} on the radio",
        "Would you mind changing the radio station to {}, please?",
        "Could you set the radio to {} for me, please?",
        "Can you switch the radio to {}?",
        "Could you dial in the radio to {} for me?"
    ]

    def get_name(self):
        return "tune_radio"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Change the station the car's radio is tuned to",
            "parameters": {
                "type": "object",
                "properties": {
                    "station": {
                        "type": "string",
                        "description": "The desired radio station to tune",
                    }
                },
                "required": ["station"],
                "returns": []
            },
        }
    
    def generate_scenario(self, template, station):
        return {
            "function": self.get_name(),
            "user_input": template.format(station),
            "expected": {
                "function": self.get_name(),
                "arguments": {
                    "station": station,
                }
            }
        }
    
    def generate_random_scenario(self):
        station = random.choice(self.stations)
        template = random.choice(self.templates)

        return self.generate_scenario(template, station)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "station" in arguments 
