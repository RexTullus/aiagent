import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from calculator.functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key missing")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Enter user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]  
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
    model='gemini-2.5-flash', contents=messages, 
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0.0),
    )

    if response.usage_metadata is not None and args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for item in response.function_calls:
            function_call_result = call_function(item, args.verbose)
            if function_call_result.parts:
                if function_call_result.parts[0].function_response:
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("function_call_result.parts[0].function_response.response empty")
            else:
                 raise Exception("function_call_result.parts returned no data")
    else:
            print(response.text)

if __name__ == "__main__":
    main()
