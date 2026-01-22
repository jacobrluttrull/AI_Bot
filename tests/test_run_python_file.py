# test_run_python_file.py

from run_python_file import run_python_file


def main():
    test_cases = [
        ("calculator", "main.py", None),
        ("calculator", "main.py", ["3 + 5"]),
        ("calculator", "tests.py", None),
        ("calculator", "../main.py", None),
        ("calculator", "nonexistent.py", None),
        ("calculator", "lorem.txt", None),
    ]

    for i, (working_dir, file_path, args) in enumerate(test_cases, start=1):
        print(f"\n--- Test {i} ---")
        print(f"run_python_file({working_dir!r}, {file_path!r}, {args!r})")
        result = run_python_file(working_dir, file_path, args)
        print(result)


if __name__ == "__main__":
    main()
