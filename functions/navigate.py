import random
from guidance import gen 

class Navigate:
    places = [
        "Home", 
        "323 Rio Del Mar Blvd", 
        "Amsterdam", 
        "Decatur", 
        "Downtown", 
        "Work", 
        "the nearest gas station", 
        "SFO", 
        "the nearest ATM" 
    ]

    templates = [
        "Navigate me to {}",
    ]

    def get_name(self):
        return "navigate"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Navigate car",
            "parameters": {
                "place": "navigation destination"
            }
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"place":"' + gen(name="place", stop='"') + '"}'

        return { "place": llm["place"] }
    
    def build_scenario(self, template, place):
        return {
            "function": self.get_name(),
            "user_input": template.format(place),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "place": place,
                }
            }
        }
    
    def build_random_scenario(self):
        place = random.choice(self.places)
        template = random.choice(self.templates)

        return self.build_scenario(template, place)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "place" in parameters
        
        
