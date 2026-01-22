# test_write_file.py

from write_file import write_file


def main():
    test_cases = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed"),
    ]

    for i, (working_dir, file_path, content) in enumerate(test_cases, start=1):
        print(f"\n--- Test {i} ---")
        print(f"write_file({working_dir!r}, {file_path!r}, {content!r})")
        result = write_file(working_dir, file_path, content)
        print(result)


if __name__ == "__main__":
    main()
