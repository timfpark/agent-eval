import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from ollama_direct import OllamaDirect

from functions.call import Call
from functions.fan_control import FanControl

def test_ollama_direct():
    functions = [Call(), FanControl()]
    backend = OllamaDirect(model_tag="phi3:3.8b-mini-instruct-4k-q4_K_M", functions=functions)

    user_prompt = "Please call Ron"

    function_call_response = backend.execute(user_prompt)

    assert function_call_response['function'] == "call"
    assert function_call_response['parameters'] == {'name': 'Ron'}