import random

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
        return {
            "name": self.get_name(),
            "description": "Lock or unlock the car doors",
            "parameters": {
                "type": "object",
                "properties": {
                    "lock": {
                        "type": "boolean",
                        "description": "True if the doors should be locked, False if they should be unlocked",
                    }
                },
                "required": ["lock"],
            },
        }
    
    def generate_scenario(self, template, lock):
        return {
            "function": self.get_name(),
            "user_input": template.format(lock),
            "expected": {
                "function": self.get_name(),
                "arguments": {
                    "lock": lock == "lock",
                }
            }
        }
    
    def generate_random_scenario(self):
        lock = random.choice(self.lock_states)
        template = random.choice(self.templates)

        return self.generate_scenario(template, lock)
    
    def are_valid_arguments(self, arguments):
        return isinstance(arguments, dict) and "lock" in arguments