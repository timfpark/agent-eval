import random

class ReadNewsTool:
    subjects = [
        "the Premier League", "large language models", "Ukraine", "college football", "the stock market", "green energy", "the Oscars"
    ]

    templates = [
        "Can you read me the latest headlines about {}?",
        "What's the latest news about {}?",
        "Could you tell me the latest about {}?",
        "What are the headlines about {}?",
        "What's happening with {}?",
        "What's new with {}?",
        "What's the latest on {}?",
        "What's the latest news on {}?",
        "What's the latest with {}?",
    ]

    def get_name(self):
        return "read_news"

    def get_definition(self):
        return {
            "name": self.get_name(),
            "description": "Read the latest news about a subject",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "number",
                        "description": "The desired news subject",
                    }
                },
                "required": ["subject"],
            },
        }
    
    def generate_scenario(self):
        subject = random.choice(self.subjects)

        template = random.choice(self.templates)
        return {
            "tool_name": self.get_name(),
            "prompt": template.format(subject),
            "expected_arguments": {
                "subject": subject,
            }
        }
