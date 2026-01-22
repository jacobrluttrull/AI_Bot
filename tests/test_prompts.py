# test_prompts.py
import subprocess

TEST_CASES = [
    (
        "read the contents of main.py",
        "Calling function: get_file_content",
    ),
    (
        "write 'hello' to main.txt",
        "Calling function: write_file",
    ),
    (
        "run main.py",
        "Calling function: run_python_file",
    ),
    (
        "list the contents of the pkg directory",
        "Calling function: get_files_info",
    ),
]


def run_case(prompt: str) -> subprocess.CompletedProcess:
    # Uses uv like your assignment runner does
    cmd = ["uv", "run", "main.py", prompt]
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> None:
    for i, (prompt, expected_substring) in enumerate(TEST_CASES, start=1):
        print("=" * 80)
        print(f"CASE {i}")
        print(f"Prompt:   {prompt}")
        print(f"Expect:   {expected_substring} (substring)")
        print("-" * 80)

        result = run_case(prompt)

        print(f"Exit code: {result.returncode}")

        stdout = result.stdout.rstrip()
        stderr = result.stderr.rstrip()

        if stdout:
            print("\nSTDOUT:")
            print(stdout)
        else:
            print("\nSTDOUT: <empty>")

        if stderr:
            print("\nSTDERR:")
            print(stderr)
        else:
            print("\nSTDERR: <empty>")

        # Simple pass/fail signal
        combined = (stdout + "\n" + stderr)
        if expected_substring in combined:
            print("\nRESULT: PASS")
        else:
            print("\nRESULT: FAIL (expected substring not found)")

    print("=" * 80)


if __name__ == "__main__":
    main()
