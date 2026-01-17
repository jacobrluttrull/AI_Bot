import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment variables")
client = OpenAI(api_key=api_key)

import json  # add at top

def run_agent_turn(messages, verbose=False, model="gpt-5-nano"):
    for _ in range(15):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=available_functions,
            tool_choice="auto",
        )

        if verbose and getattr(response, "usage", None):
            usage = response.usage
            print(f"Prompt tokens: {usage.prompt_tokens}")
            print(f"Completion tokens: {usage.completion_tokens}")
            print(f"Total tokens: {usage.total_tokens}")

        assistant_msg = response.choices[0].message
        tool_calls = assistant_msg.tool_calls or []

        assistant_entry: dict = {
            "role": "assistant",
            "content": assistant_msg.content,
        }
        if tool_calls:
            assistant_entry["tool_calls"] = tool_calls
        messages.append(assistant_entry)

        if not tool_calls:
            return assistant_msg.content or ""
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        is_test_request = "test" in (last_user or "").lower()

        for tool_call in tool_calls:
            tool_result = call_function(tool_call, verbose=verbose)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )
            if is_test_request and tool_call.function.name == "run_tests":
                return tool_result

    return "Error: Max turns exceeded."



def repl(verbose=False, model="gpt-5-nano"):
    print("Entering REPL mode. Type 'exit' to quit.")
    messages = [{"role": "system", "content": system_prompt}]
    while True:
        user_input = input("> ")
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting REPL mode.")
            break
        messages.append({"role": "user", "content": user_input})

        final_text = run_agent_turn(messages, verbose=verbose, model=model)
        print(final_text)
        print()


def main():
    print("Hello from ai-bot ")
    parser = argparse.ArgumentParser(description="AI Bot")
    parser.add_argument("user_prompt", type=str, nargs="?", help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.user_prompt:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
        ]
        final_text = run_agent_turn(messages, verbose=args.verbose)
        print(final_text)
        return
    repl(verbose=args.verbose, model="gpt-5-nano")
if __name__ == "__main__":
    main()