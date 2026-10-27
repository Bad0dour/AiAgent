import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write file to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": [
                "file_path",
                "content",
            ]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    op=os.path
    try:
        working_dir_abs = op.abspath(working_directory)
        target_file = op.normpath(op.join(working_dir_abs, file_path))
        valid_target_file = op.commonpath([working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if op.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(op.dirname(target_file), exist_ok=True)
        
        with open(target_file, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}. Try Again."