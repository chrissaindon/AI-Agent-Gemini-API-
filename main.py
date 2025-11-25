import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content



def main():
    
    load_dotenv()
    

    #Prompt Structure & sys.exit handling
    args = sys.argv[1:]
    if not args:
        print("Error: no prompt provided")
        sys.exit(1)
    
    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    
    #Flag Structure
    verbose = "--verbose" in sys.argv

    #System Prompt - hardset var.
    
    system_prompt = '''
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan.
    You can perform the following actions:

    -List files and directories
    -Read file contents

    All paths you provide should be relative to the working directory.
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    '''
    
    
    #Tools Defintion

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
        ]
    )

    
    #API Fetch + Prompt Handling + Response 

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    if response.function_calls is not None:
        for function_call_part in response.function_calls:
            print(f'Calling function: {function_call_part.name}({function_call_part.args})')

    else:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    

if __name__ == "__main__": main()