import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    current_dir = os.path.join(working_directory,directory)
    abs_path = os.path.abspath(current_dir)
    abs_path_working_dir = os.path.abspath(working_directory)
    check_if_file = os.path.isfile(abs_path)
    
    if not abs_path.startswith(abs_path_working_dir):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if check_if_file:
        return (f'Error: "{directory}" is not a directory')
    
    try:
        contents = os.listdir(abs_path)
    except Exception as e:
        return f"Error:{e}"
    entry_list = []
    for entry in contents:
        try:
            entry_path = os.path.join(abs_path, entry)
            size =os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            formatted = (f'- {entry}: file_size={size} bytes, is_dir={is_dir}')
            entry_list.append(formatted)
        except Exception as e:
            return f"Error: {e}"
    completed_contents = "\n".join(entry_list)
    return completed_contents

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. " \
                "If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
