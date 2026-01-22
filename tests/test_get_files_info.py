# python
import sys
from pathlib import Path

# Ensure project root (parent of this file's parent) is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from functions.get_files_info import get_files_info

def _print_call(work_dir, directory):
    print(f'get_files_info("{work_dir}", "{directory}"):')
    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    result = get_files_info(work_dir, directory)
    if result.startswith("Error:"):
        # error lines indented by 4 spaces
        print("    " + result)
    else:
        # normal result lines: add one extra leading space so lines start with two spaces before '-'
        for line in result.splitlines():
            if line:
                print(" " + line)
    print()  # blank line between examples

def main():
    _print_call("calculator", ".")
    _print_call("calculator", "pkg")
    _print_call("calculator", "/bin")
    _print_call("calculator", "../")

    print("To import from a subdirectory, use this syntax: from DIRNAME.FILENAME import FUNCTION_NAME\n")
    print("Where DIRNAME is the name of the subdirectory, FILENAME is the name of the file without the .py extension, and FUNCTION_NAME is the name of the function you want to import.")

if __name__ == "__main__":
    main()