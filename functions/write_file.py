from google.genai import types
from pathlib import Path

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file path relative to the working directory, creating parent directories if needed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to write the file to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        project_root = Path(__file__).resolve().parent.parent
        working_root = (project_root / working_directory).resolve()
        target = (working_root / file_path).resolve()

        try:
            target.relative_to(working_root)
        except ValueError:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        target.parent.mkdir(parents=True, exist_ok=True)

        with target.open("w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
