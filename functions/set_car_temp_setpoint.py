import random
import re
from guidance import gen 

class SetCarTemperatureSetpoint:
    temperatures = [
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75
    ]

    templates = [
        "Set the temperature to {} degrees please",
        "Please set the temperature to {}",
        "Could you adjust the thermostat to {} degrees, please?",
        "Can you set the temperature to {} degrees?",
        "Adjust the temperature to {} degrees, please.",
        "Would you mind setting the temperature to {} degrees?",
        "Could you set the thermostat to {} degrees?",
        "Please adjust the temperature to {} degrees.",
        "Can you change the temperature to {} degrees?",
        "Set the thermostat to {} degrees, please.",
        "Could you set the temperature to {} degrees?",
        "Can you please adjust the temperature to {} degrees?",
        "Can you set the temperature to {} degrees?",
        "Could you change the temp to {} degrees?",
        "I’d like the temperature at {} degrees, please.",
        "Can you please set it to {} degrees?",
        "Adjust it to {} degrees for me.",
        "Would you put the temperature at {} degrees?",
        "Can you make it {} degrees?",
        "Please set the temperature to {} degrees.",
        "Could you please change it to {} degrees?",
        "Set it at {} degrees, thanks.",
        "Would you mind putting it at {} degrees?",
        "Can you adjust it to {} degrees?",
        "Please change it to {} degrees for me.",
        "Set the air conditioner to {} degrees.",
    ]

    def get_name(self):
        return "set_car_temperature_setpoint"

    def get_definition(self):
        return  {    
            "name": self.get_name(),
            "description": "Set the desired temperature",
            "parameters": [
                {
                    "name": "temperature",
                    "type": "float",
                }
            ]
        }
    
    def generate_parameters(self, llm):
        llm = llm + '{"temperature":' + gen(regex='([0-9]*[.])?[0-9]+', name="temperature") + '}'

        temperature_generated = llm["temperature"]

        # TODO: Debug why guidance regex above is not supressing non-float characters
        temperature_generated = re.sub(r'[^0-9.]', '', temperature_generated)

        return { "temperature": float(temperature_generated) }

    
    def build_scenario(self, template, temperature):
        return {
            "function": self.get_name(),
            "user_input": template.format(temperature),
            "expected": {
                "function": self.get_name(),
                "parameters": {
                    "temperature": temperature,
                }
            }
        }
    
    def build_random_scenario(self):
        temperature = random.choice(self.temperatures)
        template = random.choice(self.templates)

        return self.build_scenario(template, temperature)
    
    def are_valid_parameters(self, parameters):
        return isinstance(parameters, dict) and "temperature" in parameters
        
        
