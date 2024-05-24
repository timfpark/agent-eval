import json
from backends.ollama_langchain import OllamaLangchain

from functions.lock_doors import LockDoors
from functions.get_car_temp_setpoint import GetCarTemperatureSetpoint
from functions.set_car_temp_setpoint import SetCarTemperatureSetpoint
from functions.tune_radio import SetRadioFrequency
from functions.unhandled_request import UnhandledRequest

def log_interaction(user_input, response):
    # Log the interaction to a file in JSON format
    interaction = {
        "user_input": user_input,
        "result": response
    }
    with open("training.json", "a") as file:
        file.write(json.dumps(interaction) + "\n")

def main():
    print("Welcome to your vehicle, feel free to make requests of me.")
    print("Press Control-D to exit.")

    functions = [LockDoors(), GetCarTemperatureSetpoint(), SetCarTemperatureSetpoint(), SetRadioFrequency(), UnhandledRequest()]
    backend = OllamaLangchain("phi3:3.8b-mini-instruct-4k-q4_K_M", functions)
    
    try:
        while True:
            user_request = input(">>> ")
            response = backend.execute(user_request)
            log_interaction(user_request, response)
            print(response)
    except EOFError:
        # Handle Control-D to exit the REPL
        print("\nExiting REPL. Goodbye!")

if __name__ == "__main__":
    main()