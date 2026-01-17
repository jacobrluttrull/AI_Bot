import subprocess
from pathlib import Path

schema_run_tests = {
    "type": "function",
    "function": {
        "name": "run_tests",
        "description": "Runs the project's test suite and returns STDOUT/STDERR and exit code.",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional extra arguments for pytest (example: ['-q']).",
                }
            },
            "required": [],
            "additionalProperties": False,
        },
    },
}
def run_tests(working_directory: str, args=None) -> str:
    """
    runs: uv run pytest <args>
    returns output and the exit code.
    :param working_directory:
    :param str:
    :param args:
    :return:
    """

    try:
        project_root = Path(__file__).resolve().parent.parent
        working_root = (project_root / working_directory).resolve()
        cmd = ["uv", "run", "pytest"]
        if args:
            cmd.extend(args)
        result = subprocess.run(
            cmd,
            cwd=working_root,
            capture_output=True,
            text=True,
            timeout=120,
        )
        stdout = result.stdout
        stderr = result.stderr
        return (
            f"Exit Code: {result.returncode}\n"
            f"STDOUT:\n{stdout}\n"
            f"STDERR:\n{stderr}"
        )
    except subprocess.TimeoutExpired:
        return "Error: Test execution timed out."
    except Exception as e:
        return f"Error: {e}"