import os 
import subprocess
from subprocess import PIPE, STDOUT
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    abs_working_dir = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:   
        result = subprocess.run((["python3", abs_file_path] + args),
                   stdout=PIPE, stderr=PIPE, 
                   cwd=abs_working_dir, timeout=30
    )
        
        if result.stderr == None and result.stdout == None:
            return "No output produced"
        
        result_string = f'STDOUT: {result.stdout}, STDERR: {result.stderr}'

        if result.returncode != 0:
            error = f'Process exited with code {result.returncode}'
            result_string = result_string + error
        
        return result_string
        


    
    except Exception as e:
        return f'Error: executing Python file: {e}'
    


#run_python_file schema

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="You can run python files from a given file path which includes optional arguments depending on the file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path which we will use to run the python file",
            ),    
        },
    ),
)