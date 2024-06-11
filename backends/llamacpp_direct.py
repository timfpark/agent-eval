import json
import guidance
from guidance import assistant, gen, models, select, system, user 
 
"""
request format

"""

class LlamaCppDirect:
    system_content_template = "You have access to the following tools:\n\n{functions_json}\n\nYou must always select one of the above tools and respond with only a JSON object matching the following schema:\n\n{\n  \"name\": <name of the selected tool>,\n  \"parameters\": <parameters for the selected tool, matching the tool's JSON schema>\n}\n"

    request_template = """
            {
                "role": "system", 
                "content": ""
            }, 
            {
                "role": "user", 
                "content": "{user_prompt}"
            },
            {
                "role": "assistant",
                "content": """

    def __init__(self, model_nickname, model_path, functions):
        self.model_nickname = model_nickname
        self.model_path = model_path
        self.functions = functions
        self.functions_dict = {function.get_name(): function for function in functions}

        self.model = models.LlamaCpp(self.model_path, echo=False, n_ctx=4096)

        with assistant():
            self.model = self.model + self.build_system_content()

    def get_config_tag(self):
        return f"llamacpp-direct:{self.model_nickname}"
    
    def build_system_content(self):
        function_definitions = [function.get_definition() for function in self.functions]
        functions_json = json.dumps(function_definitions)
    
        return "I have access to the following tools:\n\n" + functions_json + "\n\nI must always select one of the above tools and respond with ONLY a serialized JSON object matching the following schema:\n\n{\"name\":\"<selected tool name>\",\"parameters\":<parameters for the selected tool, matching the tool's JSON schema>}\n"

    def execute(self, user_prompt):
        llm = self.model

        with user():
            llm = llm + user_prompt

        with assistant():
            llm = llm + gen(name="function")

        # Markup is frequently generated with the function call JSON so just strip it
        cleaned_function = llm["function"]
        cleaned_function = cleaned_function.replace('```json', '')
        cleaned_function = cleaned_function.replace('```', '')

        print(cleaned_function)
        
        function_call = json.loads(cleaned_function)

        return {
            "function": function_call["name"],
            "parameters": function_call["parameters"]
        }