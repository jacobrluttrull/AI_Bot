# python
# File: `functions/get_file_content.py`
from pathlib import Path
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)



def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Read up to MAX_CHARS from project_root / working_directory / file_path.
    Returns the file content (with a truncation note appended if truncated),
    or an error string prefixed with 'Error:'.
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        target = (project_root / working_directory / file_path).resolve()

        # Ensure target is inside the permitted project root
        try:
            target.relative_to(project_root)
        except Exception:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not target.exists() or not target.is_file():
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with target.open("r", encoding="utf-8", errors="replace") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except Exception as e:
        return f'Error: {e}'

