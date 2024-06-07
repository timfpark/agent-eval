import json
import requests

"""
request format

"""

class OllamaDirect:
    endpoint = 'http://localhost:11434/api/chat'

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
    
    def __init__(self, model_tag, functions):
        self.model_tag = model_tag
        self.functions = functions

    def build_system_content(self, functions_json):
        return "You have access to the following tools:\n\n" + functions_json + "\n\nYou must always select one of the above tools and respond with only a JSON object matching the following schema:\n\n{\n  \"name\": <name of the selected tool>,\n  \"parameters\": <parameters for the selected tool, matching the tool's JSON schema>\n}\n"

    def build_request(self, user_prompt):
        function_definitions = [function.get_definition() for function in self.functions]
        functions_json = json.dumps(function_definitions)
        system_content = self.build_system_content(functions_json)

        return {
            "messages": [
                {
                    "role": "system", 
                    "content": system_content, 
                    "images": []
                }, 
                {
                    "role": "user", 
                    "content": user_prompt, 
                    "images": []
                }
            ], 
            "model": self.model_tag, 
            "format": "json",
            "stream": False
        }

    def get_model_tag(self):
        return self.model_tag

    def execute(self, user_prompt):
        request = self.build_request(user_prompt)
        request_json = json.dumps(request)

        # print(request_json)

        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(self.endpoint, headers=headers, data=request_json)

        function_call_response = response.json()

        print(f"function_call_response: {function_call_response}")

        message_content = json.loads(function_call_response["message"]["content"])

        print(f"decoded function: {message_content}")

        return {
            "function": message_content["name"],
            "parameters": message_content["parameters"]
        }

        """
        {
            "model": "registry.ollama.ai/library/llama3:latest",
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {
                "role": "assistant",
                "content": "Hello! How are you today?"
            },
            "done": true,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000
        }
        """

        return response