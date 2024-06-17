import json
import random

from backends.ollama_langchain import OllamaLangchain
from evaluator import evaluate_with_ollama, print_results

from functions.call import Call
from functions.fan_control import FanControl
from functions.get_car_temp_setpoint import GetCarTemperatureSetpoint
from functions.lock_doors  import LockDoors
from functions.navigate import Navigate
from functions.set_car_temp_setpoint import SetCarTemperatureSetpoint
from functions.text import Text
from functions.tune_radio import TuneRadio
from functions.volume_control import VolumeControl

model_tag = "phi3:3.8b-mini-instruct-4k-q4_K_M"
functions = [Call(), FanControl(), GetCarTemperatureSetpoint(), LockDoors(), Navigate(), SetCarTemperatureSetpoint(), Text(), TuneRadio(), VolumeControl(), PassToCloud()]
 
reproducability_seed = random.randint(1, 100000)
print(f"reproducability seed: {reproducability_seed}")
print()

random.seed(reproducability_seed)

function_count_results = {}

for function_count in range(1, len(functions)+1):
    selected_functions = functions[-function_count:]
    print(f"evaluating {model_tag} with {len(selected_functions)} functions:")
    for function in selected_functions:
        print(f"  {function.get_name()}")
    
    evaluations_per_tool = 100
    scenarios = []

    for function in selected_functions:
        for i in range(evaluations_per_tool):
            scenarios.append(function.generate_random_scenario())

    random.shuffle(scenarios)

    backend = OllamaLangchain(model_tag, selected_functions)

    function_count_results[function_count] = evaluate_with_ollama(backend, selected_functions, scenarios)

print()

print(function_count_results)

for function_count in function_count_results:
    print(f"{function_count} functions:")
    print(print_results(function_count_results[function_count]))
    print()

with open('results/tool-count-eval-m1-max.json', 'w') as file:
    json.dump(function_count_results, file)