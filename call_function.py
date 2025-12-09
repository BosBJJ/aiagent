from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.schemas import (
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
)


available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content,
                               schema_run_python_file, schema_write_file],
    )

def call_function(function_call_part: types.FunctionCall, verbose=False):
    function_call_part.args["working_directory"] = "./calculator"
    function_name = function_call_part.name
    avail_functs = {"get_file_content": get_file_content, "get_files_info": get_files_info,
                    "run_python_file": run_python_file, "write_file": write_file}
    if not verbose:
        print(f" - Calling function: {function_call_part.name}")
    else:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    if function_call_part.name in avail_functs:
        function_result = avail_functs[function_call_part.name](**function_call_part.args)
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
    else:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],
)
