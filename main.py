import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt
from functions.schemas import *
from call_function import call_function, available_functions


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


    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    try:
        for repetions in range(20):
            response = client.models.generate_content(
                    model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(
                        tools=[available_functions], system_instruction=system_prompt)
            )
            candidates = response.candidates
            for candidate in candidates:
                messages.append(candidate.content)
            if response.function_calls:
                funct_call_responses = []
                for function_call_part in response.function_calls:
                    funct_call_result = call_function(function_call_part, verbose=verbose)
                    if not funct_call_result.parts or not funct_call_result.parts[0].function_response:
                        raise Exception("empty function call result")
                    funct_response = funct_call_result.parts[0].function_response.response
                    funct_call_responses.append(funct_call_result.parts[0])
                    if verbose:
                        print(f"-> {funct_call_result.parts[0].function_response.response['result']}")
                if not funct_call_responses:
                    raise Exception("No function responses generated. Exiting.")
                tool_message = types.Content(role="user", parts=funct_call_responses)
                messages.append(tool_message)
            elif response.text:
                if verbose:
                    print("User prompt:", prompt)
                    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                    print("Response tokens:", response.usage_metadata.candidates_token_count)
                    print(response.text)
                else: 
                    print(response.text)
                break
    except Exception as e:
        print("Error while generating content", e)

if __name__ == "__main__":
    main()
