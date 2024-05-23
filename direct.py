import ollama

prompt = """
<|system|>
You are an AI assistant that can help the user with a variety of tasks. You have access to the functions provided by the schema below:

<|functions_schema|>
[
    {
        "name": "get_tweets_by_hashtag",
        "description": "Retrieves tweets containing a given hashtag",
        "parameters": [
            {
                "name": "hashtag",
                "type": "string",
            },
            {
                "name": "count",
                "type": "int",
            }
        ],
        "required": [ "hashtag" ],
        "returns": [
            {
                "name": "tweets",
                "type": "list[string]",
            }
        ]
    },
    {
        "name": "get_value_from_dict",
        "description": "Retrieves the value from a dictionary for a given key",
        "parameters": [
            {
                "name": "dictionary",
                "type": "dict[string, any]",
            },
            {
                "name": "key",
                "type": "string",
            }
        ],
        "required": [ "dictionary", "key" ],
        "returns": [
            {
                "name": "value",
                "type": "any",
            }
        ]
    },
    {
        "name": "concatanate_strings",
        "description": "Concatanates a list of strings into a single string",
        "parameters": [
            {
                "name": "list_of_strings",
                "type": "list[string]",
            }
        ],
        "required": [ "list_of_strings" ],
        "returns": [
            {
                "name": "concatanated_string",
                "type": "string",
            }
        ]
    },
    {
        "name": "get_sentiment_analysis",
        "description": "Performs sentiment analysis on a given list of strings, by calling a sentiment analysis model. Returns Positiveness Scale from -10 to +10 (1 increments)",
        "parameters": [
            {
                "name": "text",
                "type": "list[string]",
            }
        ],
        "required": [ "text" ],
        "returns": [
            {
                "name": "sentiment",
                "type": "int",
            }
        ]
    },
    {    
        "name": "get_mean",
        "description": "Calculates the mean of a list of integers",
        "parameters": [
            {
                "name": "nummbers",
                "type": "list[int]",
            }
        ],
        "required": [ "numbers" ],
        "returns": [
            {
                "name": "mean",
                "type": "float",
            }
        ]
    }.
    {
        "name": "send_email",
        "description": "Sends an email with the given subject, body, and recipient",
        "parameters": [
            {
                "name": "subject",
                "type": "string",
            },
            {
                "name": "body",
                "type": "string",
            },
            {
                "name": "recipient",
                "type": "string",
            }
        ],
        "required": [ "subject", "body", "recipient" ],
        "returns": []
    },
    {
        "name": "output_to_current_chat",
        "description": "Outputs a message to the current chat or conversation",
        "parameters": [
            {
                "name": "message",
                "type": "string",
            }
        ],
        "required": [ "message" ],
        "returns": []
    },
    {
        "name": "turn_into_string",
        "description": "Returns the string representation of a value of any data type",
        "parameters": [
            {
                "name": "value",
                "type": "any",
            }
        ],
        "required": [ "value" ],
        "returns": [
            {
                "name": "value_string",
                "type": "string",
            }
        ]
    }
] 
When the user asks you a question, if you need to use functions, provide ONLY ALL OF THE function calls, ALL IN ONE PLACE, in the format:
<|function_calls|>
[
    { "name": "function_name", "kwargs": {"kwarg_1": "value_1", "kwarg_2": "value_2"}, "returns": ["output_1"]},
    { "name": "other_function_name", "kwargs": { "kwarg_3": "$output_1$"}, "returns": ["output_2", "output_3"]},
    ...
]
<|end_function_calls|>

If you need to modify strings ONLY USE THE AVAILABLE FUNCTIONS GIVEN TO YOU. IF AND ONLY IF you don't need to use functions, give your answer in between <|answer|> and <|end_answer|> blocks. For your thoughts and reasoning behind using or not using functions, place ALL OF THEM in between a SINGLE <|thoughts|> and <|end_thoughts|> block, before the <|function_calls|> and <|end_function_calls|> tags, like so:

<|thoughts|>
The user wants X, to do that, I should call the following functions:
1. function_name: Reasoning,
2. function_name_2: Reasoning2,
3. etc.
<|end_thoughts|>

Provide nothing else than the information in the <|function_calls|> & <|end_function_calls|>, <|answer|> & <|end_answer|> and <|thoughts|> & <|end_thoughts|> blocks.<|end|>
<|user|>
Can you send my friend (jasper3131@gmail.com) an email about the current sentiment about MMA in twitter?<|end|>
<|assistant|>
"""

print(ollama.generate(model='phi3:3.8b-mini-instruct-4k-q4_K_M', prompt=prompt))