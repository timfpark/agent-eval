import json
import guidance
from guidance import assistant, gen, models, select, system, user 
 
"""
request format

"""

class TransformersGuidance:
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

    def __init__(self, model_repo, functions):
        self.model_repo = model_repo
        self.functions = functions

        # self.model = guidance.models.Transformers(
        #    self.model_repo, 
        #    trust_remote_code=True, 
        #    device_map="cuda",
        #    do_sample=True,
        #    temperature=0
        # )

        self.model = models.LlamaCpp("./Phi-3-mini-4k-instruct-q4.gguf")

        with assistant():
            self.model = self.model + self.build_system_content()

        print(self.model)

    def get_model_tag(self):
        return self.model_repo
    
    def build_system_content(self):
        function_definitions = [function.get_definition() for function in self.functions]
        functions_json = json.dumps(function_definitions)
    
        return "I have access to the following tools:\n\n" + functions_json + "\n\nI must always select one of the above tools and respond with only a JSON object matching the following schema:\n\n{\"name\":\"<name of the selected tool>\",\"parameters\":<parameters for the selected tool, matching the tool's JSON schema>}\n"

    def execute(self, user_prompt):
        function_names = [function.get_name() for function in self.functions]

        llm = self.model

        with user():
            llm = llm + user_prompt

        with assistant():
            llm = llm + '{"function":"' + select(function_names, name="function") + '",'
            llm = llm + '"parameters":' + gen(name="parameters")

        print(llm)

        parameters = llm["parameters"]
        trailing_bracket = parameters[-1]
        if trailing_bracket != "}":
            return
        
        parameters_json = parameters[:-1]

        parsed_parameters = json.loads(parameters_json)

        return {
            "function": llm["function"],
            "parameters": parsed_parameters
        }