import random

class PassToCloud:
    templates = [
        "Can you read me the latest headlines",
        "Fetch me a quote for Microsoft's current stock price",
        "Make me reservations at Mentone for 8pm on Tuesday",
        "When is my next service appointment",
        "What is the weather like in San Francisco today",
    ]

    def get_name(self):
        return "pass_to_cloud"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Handles any user requests that are not clearly handled by another more specific function above",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "returns": []
            },
        }
    

    def generate_scenario(self, template):
        return {
            "function": self.get_name(),
            "user_input": template,
            "expected": {
                "function": self.get_name(),
                "arguments": {}
            }
        }
    
    def generate_random_scenario(self):
        template = random.choice(self.templates)

        return self.generate_scenario(template)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and len(arguments) == 0
