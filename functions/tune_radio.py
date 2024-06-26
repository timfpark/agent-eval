import random
from guidance import gen 

class TuneRadio:
    stations = [
        101.7, 90.3, 94.5, 102.3, 98.5, 99.1, 100.3, 97.9, 96.7, 103.1, "KQED", "The Beach", "BBC Radio 1", "KFOG", "KISS FM", "Radio Bob"
    ]

    templates = [
        "Can you tune the radio to {} please",
        "Change the radio station to {}",
        "Please tune to {} on the radio",
        "Would you mind changing the radio station to {}, please?",
        "Could you set the radio to {} for me, please?",
        "Can you switch the radio to {}?",
        "Could you adjust the radio station to {} for me?",
        "Would you mind tuning the radio to {}?",
        "Can you please set the radio to {}?",
        "Please change the radio station to {}",
        "Can you change the radio station to {}?",
        "Please tune the radio to {}",
        "Can you tune the radio to {}?",
    ]

    def get_name(self):
        return "tune_radio"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Change the radio station",
            "parameters": [
                {
                    "name": "station",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"station":"' + gen(name="station", stop='"') + '"}'

        return { "station": llm["station"] }
    
    def build_scenario(self, template, station):
        return {
            "function": self.get_name(),
            "user_input": template.format(station),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "station": station,
                }
            }
        }
    
    def build_random_scenario(self):
        station = random.choice(self.stations)
        template = random.choice(self.templates)

        return self.build_scenario(template, station)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "station" in parameters 
