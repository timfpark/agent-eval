import json
import random

from backends.ollama_direct import OllamaDirect
from backends.llamacpp_guidance import TransformersGuidance

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
#    OllamaDirect("phi3:14b-medium-4k-instruct-q4_0", functions),
#    OllamaDirect("phi3:3.8b-mini-instruct-4k-q4_K_M", functions),
    TransformersGuidance(model_repo="microsoft/Phi-3-mini-4k-instruct", functions=functions),

#    OllamaDirect("wizardlm2:7b-q4_0", functions),
#    OllamaDirect("llama3:8b-instruct-q4_0", functions),
#    OllamaLangchain("phi3:14b-medium-128k-instruct-q4_0", functions),
]
 
seed = random.randint(1, 100000)
print(f"reproducability seed: {seed}")
print()

random.seed(seed)

evaluations_per_function = 10
scenarios = []
for function in functions:
    for i in range(evaluations_per_function):
        scenarios.append(function.build_random_scenario())

random.shuffle(scenarios)

config_results = {}
for backend in backends:
    print(f"evaluating config: {backend.get_config_tag()}")
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

print("done")