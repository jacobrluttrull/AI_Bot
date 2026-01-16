import json

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


# OpenAI expects a LIST of tools (each tool is a dict)
available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(tool_call, verbose: bool = False):
    """
    tool_call is an OpenAI tool call object.
    We return a string (or dict) that will be sent back to the model as a tool result.
    """
    function_name = tool_call.function.name or ""
    raw_args = tool_call.function.arguments or "{}"

    if verbose:
        print(f"Calling function: {function_name}({raw_args})")
    else:
        print(f" - Calling function: {function_name}")

    func = function_map.get(function_name)
    if func is None:
        return json.dumps({"error": f"Unknown function: {function_name}"})

    # Parse arguments from JSON string
    try:
        args = json.loads(raw_args)
        if not isinstance(args, dict):
            args = {}
    except json.JSONDecodeError:
        args = {}

    # Inject your working directory (same behavior as before)
    args["working_directory"] = "./calculator"

    # Call the real function
    try:
        function_result = func(**args)
        # Return a JSON string (model-friendly)
        return json.dumps({"result": function_result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)
