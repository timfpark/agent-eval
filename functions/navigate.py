import random

class Navigate:
    places = [
        "Home", "323 Rio Del Mar Blvd", "Amsterdam", "Decatur", "Downtown", "Work", "nearest gas station", "SFO", "nearest ATM" ]

    templates = [
        "Navigate me to {}",
    ]

    def get_name(self):
        return "navigate"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Navigate to specified named place",
            "parameters": [
                {
                    "name": "place",
                    "type": "string",
                }
            ],
            "required": [ "place" ],
            "returns": []
        }
    
    def generate_scenario(self, template, place):
        return {
            "function": self.get_name(),
            "user_input": template.format(place),
            "expected": {
                "function": self.get_name(),
                "arguments": {
                    "place": place,
                }
            }
        }
    
    def generate_random_scenario(self):
        place = random.choice(self.places)
        template = random.choice(self.templates)

        return self.generate_scenario(template, place)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "place" in arguments
        
        
