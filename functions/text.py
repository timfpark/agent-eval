import random
from guidance import gen 

class Text:
    names = [
        "Fiona Clarke", 
        "Anne", 
        "Elena Ramirez", 
        "Elise", 
        "Hugo", 
        "Mira", 
        "Ben", 
        "Tess", 
        "Marcus Whitmore", 
        "Eva", 
        "Christopher", 
        "Cameron", 
        "Lila", 
        "Theo", 
        "Maris", 
        "Jovan", 
        "Owen McGrath", 
        "Nadia Petrova", 
        "Matteo Rossi",
        "Alejandro Fuentes"
    ]

    messages = [
        "I am running late for dinner",
        "I am running late",
        "I will be there soon",
        "I am on my way",
        "I am stuck in traffic",
        "I am almost there",
        "I am running behind"
    ]

    templates = [
        "Please text {} that {}",
    ]

    def get_name(self):
        return "text"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Send text message to the specified contact",
            "parameters": [
                {
                    "name": "name",
                    "type": "string",
                },
                {
                    "name": "message",
                    "type": "string",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"name":"' + gen(name="name", stop='"') + '",'
        llm = llm + '{"message":"' + gen(name="message", stop='"') + '"}'

        return { "name": llm["name"], "message": llm["message"] }
    
    def build_scenario(self, template, name, message):
        return {
            "function": self.get_name(),
            "user_input": template.format(name, message),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "name": name,
                    "message": message
                }
            }
        }
    
    def build_random_scenario(self):
        name = random.choice(self.names)
        message = random.choice(self.messages)
        template = random.choice(self.templates)

        return self.build_scenario(template, name, message)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "name" in parameters and "message" in parameters
        
        
