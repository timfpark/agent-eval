import json
from langchain_experimental.llms.ollama_functions import OllamaFunctions
import random
import time

from get_current_weather import GetCurrentWeatherTool
from get_car_temp_setpoint import GetCarTemperatureSetpointTool
from set_car_temp_setpoint import SetCarTemperatureSetpointTool

def fuzzy_dict_equal(dict1, dict2):
    if dict1.keys() != dict2.keys():
        return False
    
    for key in dict1:
        val1 = dict1[key]
        val2 = dict2[key]
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if not abs(val1 - val2) < 1e-9:  # Allows a tiny difference in floating point representations
                return False
        elif val1 != val2:
            return False
    return True

# Are there user inputs that are more likely to fail?
# How do scores vary with different number of tools?
# How does latency vary with different tools?
# How does hardware effect latency (4800 vs. M2 vs M4)?
# How does latency vary by model? (phi3 vs. phi3 4bit vs. llama3?)
# How does correctness vary by model?
# What is the memory usage by model?

class Evaluator:
    def __init__(self, model, tools, scenarios):
        self.model = model
        self.tools = tools
        self.scenarios = scenarios
            
        self.results = {}

        for tool in tools:
            self.results[tool.get_name()] = {
                "passed": 0,
                "total_evaluations": 0,
                "latencies": []
            }

        # print(f"results: {self.results}")

    def evaluate_scenario(self, scenario):
        tool_name = scenario["tool_name"]
        expected_arguments = scenario["expected_arguments"]
        prompt = scenario["prompt"]

        start_time = time.time()

        response = self.model.invoke(prompt)
        
        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000.0

        self.results[tool_name]["latencies"].append(latency_ms)
        self.results[tool_name]["total_evaluations"] += 1

        function_call_response = response.additional_kwargs["function_call"]

        if function_call_response["name"] == tool_name:
            if isinstance(function_call_response["arguments"], str):
                function_call_response_arguments = function_call_response["arguments"]
                if function_call_response_arguments == '':
                    function_call_response_arguments = '{}'
                function_call_response_arguments = json.loads(function_call_response_arguments)

            if not isinstance(expected_arguments, dict):
                expected_arguments = json.loads(expected_arguments)
                
            if fuzzy_dict_equal(function_call_response_arguments, expected_arguments):
                # print(f"passed: {function_call_response} in {latency_ms}ms")
                self.results[tool_name]["passed"] += 1
#            else:
#                print(f"arguments failed: {function_call_response_arguments} vs. expected {expected_arguments}")
#        else:
#            print(f"function selection failed: {function_call_response["name"]} vs. expected {tool_name}")

    def evaluate(self):
        # warm up model
        if len(scenarios) > 0:
            self.model.invoke(scenarios[0]["prompt"])

        for scenario in self.scenarios:
            self.evaluate_scenario(scenario)

    def print_results(self):
        for tool in self.tools:
            tool_name = tool.get_name()
            if self.results[tool_name]["total_evaluations"] > 0:
                success_percentage = self.results[tool_name]["passed"] / self.results[tool_name]["total_evaluations"] * 100.0
                avg_latency_ms = sum(self.results[tool_name]["latencies"]) / len(self.results[tool_name]["latencies"])
                print(f"TOOL: {tool_name}")
                print(f"passed: {self.results[tool_name]["passed"]} of {self.results[tool_name]["total_evaluations"]} ({success_percentage}%)")
                print(f"latency: {min(self.results[tool_name]["latencies"])}ms min | {avg_latency_ms} ms avg | {max(self.results[tool_name]["latencies"])} ms max")
                print()

models = ["phi3:3.8b-mini-instruct-4k-q4_K_M"] # , "llama3:8b-instruct-q4_0", "wizardlm2:7b-q4_0"]
available_tools = [GetCurrentWeatherTool(), SetCarTemperatureSetpointTool(), GetCarTemperatureSetpointTool()]
 
reproducability_seed = random.randint(1, 100000)
print(f"reproducability_seed: {reproducability_seed}")
evaluations_per_tool = 10

for model in models:
    print(f"evaluating model {model}")

    random.seed(reproducability_seed)

    model = OllamaFunctions(
        model=model, 
        keep_alive=-1,
        format="json",
        base_url="http://localhost:11434",
    )

    for number_of_tools in range(1, len(available_tools)+1):
        print(f"evaluating with {number_of_tools} tools")

        selected_tools = random.sample(available_tools, number_of_tools)

        scenarios = []
        for tool in selected_tools:
            for i in range(evaluations_per_tool):
                scenarios.append(tool.generate_scenario())

        random.shuffle(scenarios)

        model = model.bind_tools(
            tools=[tool.get_definition() for tool in selected_tools]
        )

        evaluator = Evaluator(
            model=model,
            tools=selected_tools,
            scenarios=scenarios
        )

        evaluator.evaluate()
        evaluator.print_results()

# Generate more variants of possible user inputs

# Are there user inputs that are more likely to fail?
# How do scores vary with different number of tools?
# How does latency vary with different tools?
# How does hardware effect latency (4800 vs. M2 vs M4)?
# How does latency vary by model? (phi3 vs. phi3 4bit vs. llama3?)
# How does correctness vary by model?
# What is the memory usage by model?