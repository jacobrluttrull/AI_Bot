from pathlib import Path
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
        # NOTE: directory is optional on purpose
    ),
)

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        project_root = Path(__file__).resolve().parent.parent
        working_root = (project_root / working_directory).resolve()

        # If directory is missing/empty, treat it as "."
        if not directory:
            directory = "."

        target = (working_root / directory).resolve()

        try:
            target.relative_to(working_root)
        except Exception:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not target.exists():
            return f'Error: "{directory}" does not exist'

        if not target.is_dir():
            return f'Error: "{directory}" is not a directory'

        entries = []
        for p in sorted(target.iterdir(), key=lambda p: p.name):
            name = p.name
            size = p.stat().st_size
            is_dir = p.is_dir()
            entries.append(f' - {name}: file_size={size} bytes, is_dir={is_dir}')

        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"
