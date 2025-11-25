import os
from functions.config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(abs_file_path, "r") as text:
        file_content = text.read(MAX_CHAR)
        if os.path.getsize(abs_file_path):
            file_content = file_content + (f'[...File "{file_path}" truncated at 10000 characters]')

    return file_content


#get_file_content schema

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of files within the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to get file content from, relative to the working directory. If not provided, get content from the working directory itself.",
            ),
        },
    ),
)