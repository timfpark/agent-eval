from langchain_experimental.llms.ollama_functions import OllamaFunctions

import json
import statistics
from tabulate import tabulate
import time

def fuzzy_dict_equal(dict1, dict2):
    if dict1.keys() != dict2.keys():
        return False
    
    for key in dict1:
        val1 = dict1[key]
        val2 = dict2[key]
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if not abs(val1 - val2) < 1e-9:  # Allows a tiny difference in floating point representations
                return False
        elif str(val1).lower() != str(val2).lower():
            return False
    return True

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

    def evaluate_scenario(self, scenario):
        tool_name = scenario["tool_name"]
        expected_arguments = scenario["expected_arguments"]
        prompt = scenario["prompt"]

        start_time = time.time()

        self.results[tool_name]["total_evaluations"] += 1
        
        try:
            response = self.model.invoke(prompt)
        except Exception as e:
            print(f"failed to invoke model with prompt {prompt}")
            print(e)
            return

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000.0

        self.results[tool_name]["latencies"].append(latency_ms)
        
        function_call_response = response.additional_kwargs["function_call"]

        if function_call_response["name"] == tool_name:
            if isinstance(function_call_response["arguments"], str):
                function_call_response_arguments = function_call_response["arguments"]
                if function_call_response_arguments == '':
                    function_call_response_arguments = '{}'
                function_call_response_arguments = json.loads(function_call_response_arguments)

            if not isinstance(expected_arguments, dict):
                print(f"*** expected_arguments is not dict: {expected_arguments}")
                expected_arguments = json.loads(expected_arguments)
                
            if fuzzy_dict_equal(function_call_response_arguments, expected_arguments):
                # print(f"passed: {function_call_response} in {latency_ms}ms")
                self.results[tool_name]["passed"] += 1
            else:
                print(f"arguments failed: {function_call_response_arguments} vs. expected {expected_arguments} for prompt {prompt}")
        else:
            print(f"function selection failed: {function_call_response["name"]} vs. expected {tool_name} for prompt {prompt}")

    def evaluate(self):
        # warm up model with an unevaluated run
        if len(self.scenarios) > 0:
            try:
                prompt = self.scenarios[0]["prompt"]
                response = self.model.invoke(prompt)
            except Exception as e:
                print(f"failed to invoke model with prompt {prompt}")
                print(e)
                return

        for scenario in self.scenarios:
            self.evaluate_scenario(scenario)

        for tool in self.tools:
            tool_name = tool.get_name()
            if self.results[tool_name]["total_evaluations"] > 0:
                latencies = self.results[tool_name]["latencies"]
                self.results[tool_name]["min_latency"] = min(latencies)
                self.results[tool_name]["max_latency"] = max(latencies)
                self.results[tool_name]["mean_latency"] = sum(latencies) / len(latencies)
                self.results[tool_name]["median_latency"] = statistics.median(latencies)
                self.results[tool_name]["pass_percentage"] = (self.results[tool_name]["passed"] / self.results[tool_name]["total_evaluations"]) * 100.0

        return self.results

def print_results(tools, results):
    headers = ["tool", "passed", "total", "%", "min (ms)", "mean (ms)", "median (ms)", "max (ms)"]

    data = []
    for tool in tools:
        tool_name = tool.get_name()
        if results[tool_name]["total_evaluations"] > 0:
            passed = results[tool_name]["passed"]
            total_evaluations = results[tool_name]["total_evaluations"]
            pass_percentage = results[tool_name]["pass_percentage"]

            min_latency = results[tool_name]["min_latency"]
            max_latency = results[tool_name]["max_latency"]
            mean_latency = results[tool_name]["mean_latency"]
            median_latency = results[tool_name]["median_latency"]

            data.append([tool_name, passed, total_evaluations, pass_percentage, min_latency, mean_latency, median_latency, max_latency])  

    print(tabulate(data, headers=headers))

def evaluate_with_ollama(model_tag, tools, scenarios):
    model = OllamaFunctions(
        model=model_tag, 
        keep_alive=-1,
        format="json",
        base_url="http://localhost:11434",
    )

    model = model.bind_tools(
        tools=[tool.get_definition() for tool in tools]
    )

    evaluator = Evaluator(
        model=model,
        tools=tools,
        scenarios=scenarios
    )

    return evaluator.evaluate()
