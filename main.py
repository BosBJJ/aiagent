import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.schemas import *



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    user_input = sys.argv[1:]
    if len(user_input) == 0:
        print("No input found", file=sys.stderr)
        sys.exit(1)
    verbose =  "--verbose" in user_input
    if verbose:
        user_input.remove("--verbose")
    prompt = " ".join(user_input)

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content,
                               schema_run_python_file, schema_write_file],
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt)
    )
    if response.function_calls:
        for function_call_part in response.function_calls:
            print (f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        if verbose:
            print("User prompt:", prompt)
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
            print(response.text)
        else: 
            print(response.text)
if __name__ == "__main__":
    main()
