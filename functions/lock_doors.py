import random
from guidance import select

class LockDoors:
    lock_states = [
        "lock",
        "unlock"
    ]

    templates = [
        "Can you please {} the doors for me.",
        "Would you mind {}ing the doors?",
        "Could you {} the doors?",
        "Can you {} the doors for me?",
        "Please {} the doors.",
        "Would you {} the doors, please?",
        "Could you please {} the doors?",
    ]

    def get_name(self):
        return "lock_doors"

    def get_definition(self):
        return  {
            "name": self.get_name(),
            "description": "Lock or unlock car doors",
            "parameters": [
                {
                    "name": "lock",
                    "type": "string",
                    "allowed_values": ["lock", "unlock"]
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"lock":"' + select(self.lock_states, name="lock") + '"}'

        return { "lock": llm["lock"] }

    def build_scenario(self, template, lock):
        return {
            "function": self.get_name(),
            "user_input": template.format(lock),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "lock": lock,
                }
            }
        }
    
    def build_random_scenario(self):
        lock = random.choice(self.lock_states)
        template = random.choice(self.templates)

        return self.build_scenario(template, lock)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "lock" in parameters