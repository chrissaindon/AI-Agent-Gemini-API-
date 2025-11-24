import os
from functions.config import MAX_CHAR

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
