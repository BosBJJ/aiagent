import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    working_dir_abs = os.path.abspath(working_directory)
    combined = os.path.abspath(os.path.join(working_dir_abs,file_path))
    check_path = combined.startswith(working_dir_abs)
    check_existance = os.path.exists(combined)
    check_file = combined.endswith(".py")
    

    if not check_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not check_existance:
        return f'Error: File "{file_path}" not found.'
    if not check_file:
        return f'Error: "{file_path}" is not a Python file.'

    try: completed_process = subprocess.run(["python", file_path, *args], capture_output=True, text=True, 
                                        cwd=working_dir_abs, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if len(completed_process.stderr) == 0 and len(completed_process.stdout) == 0:
        return "No output produced"
    
    if completed_process.returncode == 0:
        return f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}'
    else:
        return f'STDOUT: {completed_process.stdout} STDERR: {completed_process.stderr}. Process exited with code {completed_process.returncode}'
    
