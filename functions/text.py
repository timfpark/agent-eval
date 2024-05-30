import random

class Text:
    names = [
        "Tim Park", "Anni", "Ron Blasko", "Sue", "Tom", "Liz", "Ben", "Tia", "Joe Long", "Eva", "Christopher", "Cameron"
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
            "description": "Send text message to the specified named contact",
            "parameters": [
                {
                    "name": "name",
                    "type": "string",
                },
                {
                    "name": "message",
                    "type": "string",
                }
            ],
            "required": [ "name", "message" ],
            "returns": []
        }
    
    def generate_scenario(self, template, name, message):
        return {
            "function": self.get_name(),
            "user_input": template.format(name, message),
            "expected": {
                "function": self.get_name(),
                "arguments": {
                    "name": name,
                    "message": message
                }
            }
        }
    
    def generate_random_scenario(self):
        name = random.choice(self.names)
        message = random.choice(self.messages)
        template = random.choice(self.templates)

        return self.generate_scenario(template, name, message)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "name" in arguments and "message" in arguments
        
        
