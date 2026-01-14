# test_prompts.py
import subprocess
import shlex

TEST_CASES = [
    (
        "read the contents of main.py",
        "get_file_content({'file_path': 'main.py'})",
    ),
    (
        "write 'hello' to main.txt",
        "write_file({'file_path': 'main.txt', 'content': 'hello'})",
    ),
    (
        "run main.py",
        "run_python_file({'file_path': 'main.py'})",
    ),
    (
        "list the contents of the pkg directory",
        "get_files_info({'directory': 'pkg'})",
    ),
]


def run_case(prompt: str) -> subprocess.CompletedProcess:
    # Uses uv like your assignment runner does
    cmd = ["uv", "run", "main.py", prompt]
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> None:
    for i, (prompt, expected) in enumerate(TEST_CASES, start=1):
        print("=" * 80)
        print(f"CASE {i}")
        print(f"Prompt:   {prompt}")
        print(f"Expect:   {expected}")
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
