import json
import random

from evaluator import evaluate_with_ollama, print_results
from tools.get_current_weather import GetCurrentWeatherTool
from tools.get_car_temp_setpoint import GetCarTemperatureSetpointTool
from tools.read_news import ReadNewsTool
from tools.set_car_temp_setpoint import SetCarTemperatureSetpointTool
from tools.tune_radio_tool import TuneRadioTool

model_tag = "phi3:3.8b-mini-instruct-4k-q4_K_M"
tools = [GetCurrentWeatherTool(), ReadNewsTool(), SetCarTemperatureSetpointTool(), GetCarTemperatureSetpointTool(), TuneRadioTool()]
 
reproducability_seed = random.randint(1, 100000)
print(f"reproducability seed: {reproducability_seed}")
print()

random.seed(reproducability_seed)

tool_count_results = {}

for tool_count in range(1, len(tools)+1):
    selected_tools = tools[:tool_count]
    print(f"evaluating {model_tag} with {len(selected_tools)} tool")
    
    evaluations_per_tool = 100
    scenarios = []

    for tool in selected_tools:
        for i in range(evaluations_per_tool):
            scenarios.append(tool.generate_scenario())

    random.shuffle(scenarios)

    tool_count_results[tool_count] = evaluate_with_ollama(model_tag, selected_tools, scenarios)

print()

print(tool_count_results)

for tool_count in tool_count_results:
    print(f"{tool_count} tools:")
    print(print_results(tools, tool_count_results[tool_count]))
    print()

with open('results/tool-count-amd-ryzen-7950x3d-rtx4800.json', 'w') as file:
    json.dump(tool_count_results, file)