from google.genai import types
import subprocess
from pathlib import Path

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file relative to the working directory and returns its STDOUT/STDERR",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        project_root = Path(__file__).resolve().parent.parent
        working_root = (project_root / working_directory).resolve()
        target = (working_root / file_path).resolve()

        try:
            target.relative_to(working_root)
        except ValueError:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not target.exists():
            return f'Error: "{file_path}" does not exist'

        if not target.is_file():
            return f'Error: "{file_path}" is not a regular file'

        if target.suffix != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", str(target)]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_root,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if not stdout and not stderr:
            return "No output produced"

        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"








