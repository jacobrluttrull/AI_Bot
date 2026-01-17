import subprocess
from pathlib import Path

schema_run_tests = {
    "type": "function",
    "function": {
        "name": "run_tests",
        "description": "Runs pytest for a given test path and returns STDOUT/STDERR plus exit code.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Which tests to run (default: tests at repo root). "
                        "Example: 'tests' or 'calculator/tests'."
                    ),
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional extra arguments for pytest (example: ['-q']).",
                },
            },
            "required": [],
            "additionalProperties": False,
        },
    },
}


def run_tests(working_directory: str, path: str = "tests", args=None) -> str:
    """
    Runs: uv run pytest <path> <args...>
    Returns output and exit code.
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        working_root = (project_root / working_directory).resolve()

        cmd = ["uv", "run", "pytest", path]
        if args:
            cmd.extend(args)

        result = subprocess.run(
            cmd,
            cwd=working_root,
            capture_output=True,
            text=True,
            timeout=120,
        )

        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        return (
            f"Exit code: {result.returncode}\n"
            f"Command: {' '.join(cmd)}\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )

    except subprocess.TimeoutExpired:
        return "Error: Test execution timed out after 120 seconds."
    except Exception as e:
        return f"Error: {e}"
