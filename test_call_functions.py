# test_functions_verbose.py
import subprocess

TEST_CASES = [
    ("List root files", "what files are in the root?"),
    ("List pkg directory", "list the contents of the pkg directory"),
    ("Read main.py", "read the contents of main.py"),
    ("Write a new file", "write 'hello from ai bot' to test_output.txt"),
    ("Run calculator tests", "run tests.py"),
]


def run_case(prompt: str) -> subprocess.CompletedProcess:
    cmd = ["uv", "run", "main.py", prompt, "--verbose"]
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> None:
    for i, (label, prompt) in enumerate(TEST_CASES, start=1):
        print("=" * 80)
        print(f"CASE {i}: {label}")
        print(f"Prompt: {prompt}")
        print("-" * 80)

        result = run_case(prompt)

        print(f"Exit code: {result.returncode}")

        if result.stdout.strip():
            print("\nSTDOUT:")
            print(result.stdout.rstrip())
        else:
            print("\nSTDOUT: <empty>")

        if result.stderr.strip():
            print("\nSTDERR:")
            print(result.stderr.rstrip())
        else:
            print("\nSTDERR: <empty>")

    print("=" * 80)


if __name__ == "__main__":
    main()
