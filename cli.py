import random

from evaluator import evaluate_with_ollama, print_results
from tools.get_current_weather import GetCurrentWeatherTool
from tools.get_car_temp_setpoint import GetCarTemperatureSetpointTool
from tools.read_news import ReadNewsTool
from tools.set_car_temp_setpoint import SetCarTemperatureSetpointTool
from tools.tune_radio_tool import TuneRadioTool

model_tags = ["llama3:8b-instruct-q4_0"] # "phi3:3.8b-mini-instruct-4k-q4_K_M"] # , "llama3:8b-instruct-q4_0", "wizardlm2:7b-q4_0"]
tools = [GetCurrentWeatherTool(), SetCarTemperatureSetpointTool(), GetCarTemperatureSetpointTool(), TuneRadioTool(), ReadNewsTool()]
 
reproducability_seed = random.randint(1, 100000)
print(f"reproducability seed: {reproducability_seed}")
print()

evaluations_per_tool = 100

random.seed(reproducability_seed)

scenarios = []
for tool in tools:
    for i in range(evaluations_per_tool):
        scenarios.append(tool.generate_scenario())

random.shuffle(scenarios)

for model_tag in model_tags:
    print(f"model: {model_tag}")
    print()

    results = evaluate_with_ollama(model_tag, tools, scenarios)
    print_results(tools, results)