from fuzzywuzzy import fuzz
from langchain_experimental.llms.ollama_functions import OllamaFunctions

import json
import statistics
from tabulate import tabulate
import time

def fuzzy_dict_equal(dict1, dict2):
    for key in dict1:
        if key not in dict2:
            return False
    
    for key in dict1:
        val1 = dict1[key]
        val2 = dict2[key]
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if not abs(val1 - val2) < 1e-9:  # Allows a tiny difference in floating point representations
                return False
        elif fuzz.partial_ratio(str(val1).lower(), str(val2).lower()) < 98:
            return False
    return True

class Evaluator:
    def __init__(self, backend, functions, scenarios):
        self.backend = backend
        self.functions = functions
        self.scenarios = scenarios
            
        self.results = {}

        for function in functions:
            self.results[function.get_name()] = {
                "passed": 0,
                "total_evaluations": 0,
                "latencies": []
            }

    def evaluate_scenario(self, scenario):
        function_name = scenario["function"]
        expected = scenario["expected"]
        user_input = scenario["user_input"]

        expected_arguments = expected["arguments"]
        expected_function = expected["function"]

        start_time = time.time()

        self.results[function_name]["total_evaluations"] += 1
        
        try:
            response = self.backend.execute(user_input)
        except Exception as e:
            print(f"failed to invoke model with user_input {user_input}")
            print(e)
            return

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000.0

        self.results[function_name]["latencies"].append(latency_ms)
        
        if response["function"] == expected_function:
            if isinstance(response["arguments"], str):
                if response["arguments"] == '':
                    response["arguments"] = '{}'
                response["arguments"] = json.loads(response["arguments"])

            if not isinstance(expected_arguments, dict):
                print(f"*** expected_arguments is not dict: {expected_arguments}")
                expected_arguments = json.loads(expected_arguments)
                
            if fuzzy_dict_equal(expected_arguments, response["arguments"]):
                self.results[function_name]["passed"] += 1
            else:
                print(f"arguments failed: {response["arguments"]} vs. expected {expected_arguments} for prompt '{user_input}'")
        else:
            print(f"function selection failed: '{response["function"]}' vs. expected '{expected_function}' for prompt '{user_input}'")

    def evaluate(self):
        # warm up model with an unevaluated run
        if len(self.scenarios) > 0:
            try:
                user_input = self.scenarios[0]["user_input"]
                self.backend.execute(user_input)
            except Exception as e:
                print(f"failed to invoke model with user_input {user_input}")
                print(e)
                return

        count = 0
        for scenario in self.scenarios:
            count += 1
            self.evaluate_scenario(scenario)
            print(f"{count} of {len(self.scenarios)}")

        for function in self.functions:
            function_name = function.get_name()
            if self.results[function_name]["total_evaluations"] > 0:
                latencies = self.results[function_name]["latencies"]
                self.results[function_name]["min_latency"] = min(latencies)
                self.results[function_name]["max_latency"] = max(latencies)
                self.results[function_name]["mean_latency"] = sum(latencies) / len(latencies)
                self.results[function_name]["median_latency"] = statistics.median(latencies)
                self.results[function_name]["pass_percentage"] = (self.results[function_name]["passed"] / self.results[function_name]["total_evaluations"]) * 100.0

        return self.results

def print_results(results):
    headers = ["functions", "passed", "total", "%", "min (ms)", "mean (ms)", "median (ms)", "max (ms)"]

    data = []
    for pivot in results:
        pivot_results = results[pivot]
        if pivot_results["total_evaluations"] > 0:
            passed = pivot_results["passed"]
            total_evaluations = pivot_results["total_evaluations"]
            pass_percentage = pivot_results["pass_percentage"]

            min_latency = pivot_results["min_latency"]
            max_latency = pivot_results["max_latency"]
            mean_latency = pivot_results["mean_latency"]
            median_latency = pivot_results["median_latency"]

            data.append([pivot, passed, total_evaluations, pass_percentage, min_latency, mean_latency, median_latency, max_latency])  

    print(tabulate(data, headers=headers))

def evaluate_with_ollama(backend, functions, scenarios):
    evaluator = Evaluator(
        backend=backend,
        functions=functions,
        scenarios=scenarios
    )

    return evaluator.evaluate()
