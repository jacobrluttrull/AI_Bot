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
            parts=[types.Part(text=args.user_prompt)],
        )
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=[system_prompt],
            ),
        )

        # NEW: add candidates to conversation history
        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            if candidate.content is not None:
                messages.append(candidate.content)

        function_calls = getattr(response, "function_calls", None)

        # If the model did NOT request any tools, we're done
        if not function_calls:
            if args.verbose:
                usage = getattr(response, "usage_metadata", None)
                prompt_tokens = getattr(usage, "prompt_token_count", None) if usage else None
                response_tokens = getattr(usage, "candidates_token_count", None) if usage else None

                print(f"User prompt: {args.user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

            print(response.text)
            break

        # Otherwise: run tool calls and add tool results back to the conversation
        function_results = []

        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            if not function_call_result.parts:
                raise RuntimeError("Tool result had no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Tool result part had no function_response")

            if function_response.response is None:
                raise RuntimeError("FunctionResponse.response was None")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_response.response}")

        # NEW: per instructions, append tool results as role="user"
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print("Error: Reached max iterations (20) without a final response.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
