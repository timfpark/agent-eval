import json
import random

from evaluator import evaluate_with_ollama, print_results
from tools.get_current_weather import GetCurrentWeatherTool
from tools.get_car_temp_setpoint import GetCarTemperatureSetpointTool
from tools.read_news import ReadNewsTool
from tools.set_car_temp_setpoint import SetCarTemperatureSetpointTool
from tools.tune_radio_tool import TuneRadioTool

model_tags = ["phi3:3.8b-mini-instruct-4k-q4_K_M", "llama3:8b-instruct-q4_0", "wizardlm2:7b-q4_0"]
tools = [ReadNewsTool(), GetCurrentWeatherTool(), SetCarTemperatureSetpointTool(), GetCarTemperatureSetpointTool(), TuneRadioTool()]
 
reproducability_seed = random.randint(1, 100000)
print(f"reproducability seed: {reproducability_seed}")
print()

random.seed(reproducability_seed)

evaluations_per_tool = 100
scenarios = []
for tool in tools:
    for i in range(evaluations_per_tool):
        scenarios.append(tool.generate_scenario())

random.shuffle(scenarios)

model_results = {}
for model_tag in model_tags:
    print(f"evaluating model: {model_tag}")
    model_results[model_tag] = evaluate_with_ollama(model_tag, tools, scenarios)

print()
for model_tag in model_results:
    print(model_tag)
    print(print_results(tools, model_results[model_tag]))
    print()

with open('results/model-eval-amd-ryzen-7950x3d-rtx4800.json', 'w') as file:
    json.dump(model_results, file)