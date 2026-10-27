import os
import subprocess
from subprocess import *

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file in a specified directory relative to the working directory, and includes any optional necessary arguments to run it with",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to python file, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type":"string",
                    },
                    "description": "List of arguments to be run in addition with the run command",
                },
            },
            "required": [
                "file_path",
            ],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    op = os.path
    try:
        working_dir_abs = op.abspath(working_directory)
        target_file = op.normpath(op.join(working_dir_abs, file_path))
        valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not op.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file' 
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command: list[str] = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, cwd=working_dir_abs, text=True, timeout=30, capture_output=True)
        code = completed_process.returncode
        stdout = completed_process.stdout
        stderr = completed_process.stderr

        return_string = []
        if code != 0:
            return_string.append(f"Process exited with code {code}")
        if stdout != "":
            return_string.append(f"STDOUT: {stdout}")
        if stderr != "":
            return_string.append(f"STDERR: {stderr}")
        if stdout == "" and stderr == "": 
            return_string.append("No output produced")
        return ''.join(return_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"