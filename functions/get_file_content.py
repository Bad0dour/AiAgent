import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Shows content inside of a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get content from, relative to the working directory",
                },
            },
            "required" : [
                "file_path",
            ]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    op=os.path
    try:
        working_dir_abs = op.abspath(working_directory)
        target_file = op.normpath(op.join(working_dir_abs, file_path))
        valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if op.isdir(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    except Exception as e:
        return f"Error: {e}. Try Again."