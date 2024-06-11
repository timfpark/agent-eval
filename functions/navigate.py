import random
from guidance import gen 

class Navigate:
    destinations = [
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
            "description": "Navigate",
            "parameters": [
                {
                    "name": "destination",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"destination":"' + gen(name="destination", stop='"') + '"}'

        return { "destination": llm["destination"] }
    
    def build_scenario(self, template, destination):
        return {
            "function": self.get_name(),
            "user_input": template.format(destination),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "destination": destination,
                }
            }
        }
    
    def build_random_scenario(self):
        destination = random.choice(self.destinations)
        template = random.choice(self.templates)

        return self.build_scenario(template, destination)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "destination" in parameters
        
        
