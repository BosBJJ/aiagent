import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    check_if_in_dir = full_path.startswith(abs_working_dir)

    if not check_if_in_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        dir_name = os.path.dirname(full_path)
        os.makedirs(dir_name, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
    
    