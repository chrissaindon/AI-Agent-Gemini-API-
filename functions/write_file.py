import os
from google.genai import types

def write_file(working_directory, file_path, content):
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        directory = os.path.dirname(abs_file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
    
    with open(abs_file_path, "w") as file:
        file.write(content)
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



#write_file schema

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="You can write and overwrite content; given as a string to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path in which we will use to write the provided content too",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string of text that will be written or overwritten into the file in file_path",
            ),
        },
    ),
)