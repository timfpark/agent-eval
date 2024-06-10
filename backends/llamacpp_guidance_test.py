import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from backends.llamacpp_guidance import TransformersGuidance

from functions.call import Call
from functions.fan_control import FanControl

def test_transformers_guidance():
    functions = [Call(), FanControl()]
    backend = TransformersGuidance(model_repo="microsoft/Phi-3-mini-4k-instruct", functions=functions)

    user_prompt = "Please call Ron"

    function_call_response = backend.execute(user_prompt)

    assert function_call_response['function'] == "call"
    assert function_call_response['parameters'] == {'name': 'Ron'}