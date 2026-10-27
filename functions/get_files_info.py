import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    op = os.path
    try:
        working_dir_abs = op.abspath(working_directory)
        target_dir = op.normpath(op.join(working_dir_abs, directory))
        valid_target_dir = op.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not op.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        print(f'Success: "{directory}" is within the working directory')
        return "\n".join([f"- {file}: file_size={op.getsize(op.join(target_dir,file))} bytes, is_dir={op.isdir(op.join(target_dir,file))}" for file in os.listdir(target_dir)])

    except Exception as e:
        return f"Error: directories are invalid: {e}. Try Again."
