import random
from guidance import gen 

class Call:
    names = [
        "Tim Park", "Anni", "Ron Blasko", "Sue", "Tom", "Liz", "Ben", "Tia", "Joe Long", "Eva", "Christopher", "Cameron"
    ]

    templates = [
        "Please call {}",
    ]

    def get_name(self):
        return "call"

    def get_definition(self):
        return  {
            "name": self.get_name(),
            "description": "Make phone call to the specified named contact",
            "parameters": [
                {
                    "name": "name",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"name":"' + gen(name="name", stop='"') + '"}'

        return { "name": llm["name"] }
    
    def build_scenario(self, template, name):
        return {
            "function": self.get_name(),
            "user_input": template.format(name),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "name": name,
                }
            }
        }
    
    def build_random_scenario(self):
        name = random.choice(self.names)
        template = random.choice(self.templates)

        return self.build_scenario(template, name)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "name" in parameters
        
        
