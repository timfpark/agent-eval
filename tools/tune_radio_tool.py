import random

class TuneRadioTool:
    frequencies = [
        101.7, 90.3, 94.5, 102.3, 98.5, 99.1, 100.3, 97.9, 96.7, 103.1
    ]

    templates = [
        "Can you tune the radio to {} please",
        "Change the radio station to {}",
        "Please go to {} on the radio",
        "Would you mind changing the radio station to {}, please?",
        "Could you set the radio to {} for me, please?",
        "Can you switch the radio to {}?",
        "Could you dial in the radio to {} for me?"
    ]

    def get_name(self):
        return "set_radio_station"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Select a station on the car's radio",
            "parameters": {
                "type": "object",
                "properties": {
                    "frequency": {
                        "type": "number",
                        "description": "The desired station's FM frequency",
                    }
                },
                "required": ["frequency"],
            },
        }
    
    def generate_scenario(self):
        frequency = random.choice(self.frequencies)
        template = random.choice(self.templates)
        return {
            "tool_name": self.get_name(),
            "prompt": template.format(frequency),
            "expected_arguments": {
                "frequency": frequency,
            }
        }
