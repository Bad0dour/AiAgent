import json
from collections.abc import Callable
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions: list = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

def call_function(tool_call, verbose: bool = False) -> dict:
    func_id = tool_call.id
    func_name: str = tool_call.function.name
    func_args: dict = json.loads(tool_call.function.arguments or "{}")

    return_dict = {
        "role": "tool",
        "tool_call_id": func_id,
        "content": None
    }
    
    if verbose:
        print(f" — Calling function: {func_name}({func_args})")
    else:
        print(f" — Calling function: {func_name}")

    if func_name not in function_map:
        result = f"Error: Unknown function: {func_name}"
    else:
        func_args["working_directory"] = "./calculator"
        result = function_map[func_name](**func_args)
        
    return_dict["content"] = result
    return return_dict
    
    