from langchain_experimental.llms.ollama_functions import OllamaFunctions

class OllamaLangchain:
    def __init__(self, model_tag, functions):
        self.model_tag = model_tag

        model = OllamaFunctions(
            model=model_tag, 
            keep_alive=-1,
            format="json",
            base_url="http://localhost:11434",
        )

        self.model = model.bind_tools(
            tools=[function.get_definition() for function in functions]
        )
        
    def get_model_tag(self):
        return self.model_tag
    
    def execute(self, user_prompt):
        response = self.model.invoke(user_prompt)
        
        function_call_response = response.additional_kwargs["function_call"]

        return {
            "function": function_call_response["name"],
            "arguments": function_call_response["arguments"]
        }
