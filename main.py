import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

client = genai.Client(api_key=api_key)


def main():
    print("Hello from ai-bot!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()




    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=args.user_prompt)]
        )
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    usage = getattr(response, "usage_metadata", None)
    prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
    response_tokens = getattr(usage, "candidates_token_count", None) if usage else None

    function_calls = getattr(response, "function_calls", None)

    if function_calls:
        function_results = []

        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            # 1) Content must have parts
            if not function_call_result.parts:
                raise RuntimeError("Tool result had no parts")

            # 2) First part must have function_response
            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Tool result part had no function_response")

            # 3) function_response must have .response
            if function_response.response is None:
                raise RuntimeError("FunctionResponse.response was None")

            # 4) Store the first Part for later
            function_results.append(function_call_result.parts[0])

            # 5) Verbose: print the actual tool result payload
            if args.verbose:
                print(f"-> {function_response.response}")

    else:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        print(response.text)


if __name__ == "__main__":
    main()
