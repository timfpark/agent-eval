import random

class UnhandledRequest:
    templates = [
        "Can you read me the latest headlines?",
        "Fetch me a quote for Microsoft's current stock price",
        "Make me reservations at Mentone for 8pm on Tuesday",
    ]

    def get_name(self):
        return "pass_to_cloud"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Handles any requests that are not clearly handled by another more specific tool",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
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