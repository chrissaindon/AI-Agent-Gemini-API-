import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function



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
    -Execute Python files with optional arguments
    -Write or overwrite files

    All paths you provide should be relative to the working directory.
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    '''
    
    
    #Tools Defintion

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
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
        func_call_list = []
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=verbose)
        
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Fatal error: no result given")
        
            else:
                func_call_list.append(function_call_result.parts[0])
            
            
            if verbose:    
                print(f"-> {function_call_result.parts[0].function_response.response}")
                print(func_call_list)

    else:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    

if __name__ == "__main__": main()