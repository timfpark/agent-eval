import json
import guidance 
from transformers import AutoModelForCausalLM, AutoTokenizer

"""
request format

"""

class TransformersGuidance:
    system_content_template = "You have access to the following tools:\n\n{functions_json}\n\nYou must always select one of the above tools and respond with only a JSON object matching the following schema:\n\n{\n  \"name\": <name of the selected tool>,\n  \"parameters\": <parameters for the selected tool, matching the tool's JSON schema>\n}\n"

    request_template = {
        "messages": [
            {
                "role": "system", 
                "content": "", 
                "images": []
            }, 
            {
                "role": "user", 
                "content": "{user_prompt}", 
                "images": []
            }
        ], 
        "model": "{model_tag}", 
        "format": "json",
        "keep_alive": "5m",
        "stream": False
    }
    
    def __init__(self, model_repo, functions):
        self.model_repo = model_repo
        self.functions = functions

        self.model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

        # self.model = guidance.models.Transformers(
        #    self.model_repo, 
        #    trust_remote_code=True, 
        #    device_map="mps",
        #    temperature=0
        # )

    def build_system_content(self, functions_json):
        return "You have access to the following tools:\n\n" + functions_json + "\n\nYou must always select one of the above tools and respond with only a JSON object matching the following schema:\n\n{\n  \"name\": <name of the selected tool>,\n  \"parameters\": <parameters for the selected tool, matching the tool's JSON schema>\n}\n"

    def execute(self, user_prompt):
        
        return {
            "function": "call",
            "parameters": {'name': 'Ron'}
        }