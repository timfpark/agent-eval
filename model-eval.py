import json
import random

from backends.ollama_direct import OllamaDirect
from backends.llamacpp_direct import LlamaCppDirect
from backends.llamacpp_guidance import LlamaCppGuidance

from evaluator import Evaluator, print_results

from functions.call import Call
from functions.fan_control import FanControl
from functions.get_car_temp_setpoint import GetCarTemperatureSetpoint
from functions.lock_doors  import LockDoors
from functions.navigate import Navigate
from functions.set_car_temp_setpoint import SetCarTemperatureSetpoint
from functions.text import Text
from functions.tune_radio import TuneRadio
from functions.volume_control import VolumeControl

functions = [Call(), FanControl(), GetCarTemperatureSetpoint(), LockDoors(), Navigate(), SetCarTemperatureSetpoint(), Text(), TuneRadio(), VolumeControl()]
backends = [
    LlamaCppGuidance(model_nickname="phi3-mini-4k-instruct-q4", model_path="./Phi-3-mini-4k-instruct-q4.gguf", functions=functions),
    LlamaCppGuidance(model_nickname="phi3-medium-4k-instruct-q4", model_path="./Phi-3-medium-4k-instruct-Q4_K_M.gguf", functions=functions),
    LlamaCppGuidance(model_nickname="llama3-8b-instruct-q4", model_path="./Meta-Llama-3-8B-Instruct.Q4_0.gguf", functions=functions),
    LlamaCppDirect(model_nickname="phi3-mini-4k-instruct-q4", model_path="./Phi-3-mini-4k-instruct-q4.gguf", functions=functions),
    OllamaDirect(model_nickname="phi3-mini-4k-instruct-q4", model_tag="phi3:3.8b-mini-instruct-4k-q4_K_M", functions=functions),
]
 
seed = random.randint(1, 100000)

print(f"reproducability seed: {seed}")
print()

random.seed(seed)

evaluations_per_function = 200
scenarios = []
for function in functions:
    for i in range(evaluations_per_function):
        scenarios.append(function.build_random_scenario())

random.shuffle(scenarios)

config_results = {}
for backend in backends:
    evaluator = Evaluator(
        backend=backend,
        functions=functions,
        scenarios=scenarios
    )

    config_results[backend.get_config_tag()] = evaluator.evaluate()

print()

for config_tag in config_results:
    print(f"results for configuration: {config_tag}")
    print_results(config_results[config_tag])
    print()

print('dumping results to file')
with open('results/model-eval-amd-7950x3d-rtx4080.json', 'w') as file:
    json.dump(config_results, file)

# TODO
# Simplify tool definitions if using guidance (don't need parameter definitions since we drive that directly in code?)
# How can we more rigorously capture memory utilization (both CPU and GPU)?
# Expand response to allow for returning multiple functions
# More complex user inputs that need multiple functions to accomplish
# End to end testing - user input -> function calls -> update internal state -> check end state
