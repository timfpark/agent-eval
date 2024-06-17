import json
import pyaudio
from RealtimeSTT import AudioToTextRecorder
import random

from functions.call import Call
from functions.fan_control import FanControl
from functions.get_car_temp_setpoint import GetCarTemperatureSetpoint
from functions.lock_doors  import LockDoors
from functions.navigate import Navigate
from functions.set_car_temp_setpoint import SetCarTemperatureSetpoint
from functions.text import Text
from functions.tune_radio import TuneRadio
from functions.volume_control import VolumeControl

if __name__ == '__main__':
    p = pyaudio.PyAudio()

    device_count = p.get_device_count()
    first_input_device_index = None

    for i in range(device_count):
        device_info = p.get_device_info_by_index(i)
        print(f"Device {i}: {device_info['name']}")
        print(f"    - Index: {device_info['index']}")
        print(f"    - Channels: {device_info['maxInputChannels']} input, {device_info['maxOutputChannels']} output")
        print(f"    - Default Sample Rate: {device_info['defaultSampleRate']}")
        print(f"    - Host API: {p.get_host_api_info_by_index(device_info['hostApi'])['name']}")
        print()

        if not first_input_device_index and device_info['maxInputChannels'] > 0:
            first_input_device_index = device_info['index']

    print(f"Using device index {first_input_device_index} for input")

    p.terminate()

    functions = [Call(), FanControl(), GetCarTemperatureSetpoint(), LockDoors(), Navigate(), SetCarTemperatureSetpoint(), Text(), TuneRadio(), VolumeControl()]

    scenarios_per_function = 1
    user_commands = set()
    for function in functions:
        for i in range(scenarios_per_function):
            scenario = function.build_random_scenario()
            user_commands.add(scenario["user_input"])

    user_commands = list(user_commands)

    random.shuffle(user_commands)
    
    responses = {}

    for user_command in user_commands:
        with AudioToTextRecorder(input_device_index=first_input_device_index) as recorder:
            print(f"you say: {user_command}")
            transcribed_text = recorder.text()
            print(f"i heard: {transcribed_text}")

            responses[user_command] = transcribed_text

            print()

    with open('stt.json', 'r') as file:
        variants = json.load(file)
        for user_command in responses:
            variant = responses[user_command]
            if user_command not in variants:
                variants[user_command] = {}
            if variant not in variants[user_command]:
                variants[user_command][variant] =  1
            else:
                variants[user_command][variant] += 1
                
    with open('stt.json', 'w') as file:
        json.dump(variants, file)