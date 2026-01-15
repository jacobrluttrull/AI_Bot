# test_loop_prompt.py
import subprocess


def main() -> None:
    prompt = "Explain how the calculator renders the result to the console."

    result = subprocess.run(
        ["uv", "run", "main.py", prompt],
        capture_output=True,
        text=True,
    )

    print("Exit code:", result.returncode)

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


if __name__ == "__main__":
    main()
