import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import system_prompt

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

response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt)
)
if verbose:
    print("User prompt:", prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)
else: 
    print(response.text)

def main():
    print("Until next time!! - Bobs self aware AI")


if __name__ == "__main__":
    main()
