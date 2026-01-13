from pathlib import Path


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
