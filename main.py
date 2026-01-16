import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables")

client = OpenAI(api_key=api_key)


def main():
    print("Hello from ai-bot!")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=available_functions,
            tool_choice="auto",
        )

        if args.verbose and getattr(response, "usage", None):
            usage = response.usage
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Completion tokens: {usage.completion_tokens}")
            print(f"Total tokens: {usage.total_tokens}")

        assistant_msg = response.choices[0].message
        tool_calls = assistant_msg.tool_calls or []

        # Append assistant message (only include tool_calls key if present)
        assistant_entry = {"role": "assistant", "content": assistant_msg.content}
        if tool_calls:
            assistant_entry["tool_calls"] = tool_calls
        messages.append(assistant_entry)

        # If no tool calls, we're done
        if not tool_calls:
            print(assistant_msg.content or "")
            break

        # Execute each tool call and append tool results
        for tool_call in tool_calls:
            tool_result = call_function(tool_call, verbose=args.verbose)

            if not isinstance(tool_result, str):
                tool_result = json.dumps(tool_result, ensure_ascii=False)

            if args.verbose:
                print(f"-> tool({tool_call.function.name}) result: {tool_result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
    else:
        print("Error: Reached max iterations (20) without a final response.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
