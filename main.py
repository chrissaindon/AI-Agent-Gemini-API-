import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys



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


    
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model = 'gemini-2.0-flash-001', 
        contents = messages,
    )


    if verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count) 
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
    else: 
        print("Response:")
        print(response.text)

if __name__ == "__main__": main()