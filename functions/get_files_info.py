# python
# File: `functions/get_files_info.py`
from pathlib import Path

def get_files_info(work_dir: str, directory: str) -> str:
    """
    List items under project_root / work_dir / directory.
    Return lines like:
     - name: file_size=123 bytes, is_dir=False
    Or return an error string prefixed with 'Error:'.
    """
    try:
        project_root = Path(__file__).resolve().parent.parent
        target = (project_root / work_dir / directory).resolve()

        # Ensure target is inside the permitted project root
        try:
            target.relative_to(project_root)
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
        return f'Error: {e}'


