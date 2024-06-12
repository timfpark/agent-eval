from fuzzywuzzy import fuzz

import json
import statistics
from tabulate import tabulate
import time
import traceback

def fuzzy_dict_equal(dict1, dict2):
    for key in dict1:
        if key not in dict2:
            return False
    
    for key in dict1:
        val1 = dict1[key]
        val2 = dict2[key]
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if not abs(val1 - val2) < 1e-9:
                return False
        elif fuzz.partial_ratio(str(val1).lower(), str(val2).lower()) < 98:
            return False
    return True

def parse_parameters(parameters):
    if isinstance(parameters, str):
        if parameters == '':
            parameters = '{}'
        parameters = json.loads(parameters)

    return parameters

class Evaluator:
    def __init__(self, backend, functions, scenarios):
        self.backend = backend
        self.functions = functions
        self.scenarios = scenarios
            
        self.results = {}

        for function in functions:
            self.results[function.get_name()] = {
                "passed": 0,
                "function_incorrect": 0,
                "parameters_incorrect": 0,
                "non_function_response": 0,
                "total_evaluations": 0,
                "incorrect_but_valid": 0,
                "latencies": [],
                "errors": []
            }

    def evaluate_scenario(self, scenario):
        function_name = scenario["function"]
        expected = scenario["expected"]
        user_input = scenario["user_input"]

        expected_parameters = expected["parameters"]
        expected_function = expected["function"]

        start_time = time.time()

        self.results[function_name]["total_evaluations"] += 1

        try:
            print(f"evaluating user prompt: '{user_input}'")
            response = self.backend.execute(user_input)
        except Exception as e:
            self.results[function_name]["non_function_response"] += 1
            
            end_time = time.time()
            latency_ms = (end_time - start_time) * 1000.0
            self.results[function_name]["latencies"].append(latency_ms)

            print(f"failed to invoke model with user_input {user_input}")
            stack_trace = traceback.format_exc()
            print(f"exception returned: {e}")
            print("stack trace:")
            print(stack_trace)
            return "(n/a) "

        end_time = time.time()
        latency_ms = (end_time - start_time) * 1000.0
        self.results[function_name]["latencies"].append(latency_ms)

        response["parameters"] = parse_parameters(response["parameters"])

        print(f"function generated: {response["function"]} vs. expected: {expected_function}")
        print(f"parameters generated: {response["parameters"]} vs. expected: {expected_parameters}")

        if response["function"] == expected_function:
            if not isinstance(expected_parameters, dict):
                expected_parameters = json.loads(expected_parameters)
                
            if fuzzy_dict_equal(expected_parameters, response["parameters"]):
                self.results[function_name]["passed"] += 1
            else:
                print(f"PARAMETER GENERATION FAILED: {response["parameters"]} vs. expected {expected_parameters} for prompt '{user_input}'")

                self.results[function_name]["errors"].append({
                    "user_input": user_input,
                    "expected_function": expected_function,
                    "generated_function": response["function"],
                    "expected_parameters": expected_parameters,
                    "generated_parameters": response["parameters"]
                })

                self.results[function_name]["parameters_incorrect"] += 1
        else:
            print(f"FUNCTION GENERATION FAILED: '{response["function"]}' vs. expected '{expected_function}' for prompt '{user_input}'")

            self.results[function_name]["function_incorrect"] += 1
            self.results[function_name]["errors"].append({
                "user_input": user_input,
                "expected_function": expected_function,
                "generated_function": response["function"],
                "expected_parameters": expected_parameters,
                "generated_parameters": response["parameters"]
            })

            for function in self.functions:
                if function.get_name() == response["function"] and function.are_valid_parameters(response["parameters"]):
                    print(f"incorrect but valid function call returned to: {function.get_name()} with parameters: {response["parameters"]}")
                    self.results[function_name]["incorrect_but_valid"] += 1
                    break

        return latency_ms

    def evaluate(self):
        config_tag = self.backend.get_config_tag()

        # warm up model with an unevaluated run
        if len(self.scenarios) > 0:
            try:
                user_input = self.scenarios[0]["user_input"]
                print(f"warming up config {config_tag}")
                self.backend.execute(user_input)
            except Exception as e:
                print(f"failed to invoke model with user prompt {user_input}")
                print(f"exception returned: {e}")

        count = 0
        for scenario in self.scenarios:
            count += 1
            latency = self.evaluate_scenario(scenario)
            print(f"{config_tag}: {count} of {len(self.scenarios)}: {latency}ms")

        for function in self.functions:
            function_name = function.get_name()
            if self.results[function_name]["total_evaluations"] > 0:
                latencies = self.results[function_name]["latencies"]

                if latencies:
                    self.results[function_name]["min_latency"] = min(latencies)
                    self.results[function_name]["max_latency"] = max(latencies)
                    self.results[function_name]["mean_latency"] = sum(latencies) / len(latencies)
                    self.results[function_name]["median_latency"] = statistics.median(latencies)
                    self.results[function_name]["pass_percentage"] = (self.results[function_name]["passed"] / self.results[function_name]["total_evaluations"]) * 100.0
                else:
                    self.results[function_name]["min_latency"] = "-"
                    self.results[function_name]["max_latency"] = "-"
                    self.results[function_name]["mean_latency"] = "-"
                    self.results[function_name]["median_latency"] = "-"
                    self.results[function_name]["pass_percentage"] = "-"
                    
        return self.results

def print_results(results):
    headers = ["functions", "passed", "fi", "pi", "nfr", "i(bvfc)", "total", "%", "min (ms)", "mean (ms)", "median (ms)", "max (ms)"]

    data = []
    for pivot in results:
        pivot_results = results[pivot]
        if pivot_results["total_evaluations"] > 0:
            passed = pivot_results["passed"]
            function_incorrect = pivot_results["function_incorrect"]
            parameters_incorrect = pivot_results["parameters_incorrect"]
            non_function_response = pivot_results["non_function_response"]
            total_evaluations = pivot_results["total_evaluations"]
            incorrect_but_valid = pivot_results["incorrect_but_valid"]
            pass_percentage = pivot_results["pass_percentage"]

            min_latency = pivot_results["min_latency"]
            max_latency = pivot_results["max_latency"]
            mean_latency = pivot_results["mean_latency"]
            median_latency = pivot_results["median_latency"]

            data.append([pivot, passed, function_incorrect, parameters_incorrect, non_function_response, incorrect_but_valid, total_evaluations, pass_percentage, min_latency, mean_latency, median_latency, max_latency])  

    print(tabulate(data, headers=headers))
