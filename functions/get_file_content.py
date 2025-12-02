import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    combined_abs_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    check_path = combined_abs_path.startswith(abs_working_dir)

    if not check_path:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(combined_abs_path):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    
    try:
        with open(combined_abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                trunc_file = file_content_string[:MAX_CHARS]
                return trunc_file + f'[...File "{file_path}" truncated at {MAX_CHARS}]'
            return file_content_string
    except Exception as e:
        return (f"Error: {e}")
    