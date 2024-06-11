import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backends.llamacpp_guidance import LlamaCppGuidance

from functions.call import Call
from functions.fan_control import FanControl

def test_llamacpp_guidance():
    functions = [Call(), FanControl()]
    backend = LlamaCppGuidance(model_nickname="phi3-mini-4k-instruct", model_path="./Phi-3-mini-4k-instruct-q4.gguf", functions=functions)

    user_prompt = "Please call Ron"

    function_call_response = backend.execute(user_prompt)

    assert function_call_response['function'] == "call"
    assert function_call_response['parameters'] == {'name': 'Ron'}