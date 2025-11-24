import os

def get_files_info(working_directory, directory="."):   
    os.listdir(working_directory)

    joined_path = os.path.join(working_directory, directory)
    abs_joined_path = os.path.abspath(joined_path)
    abs_working_dir = os.path.abspath(working_directory)
    
    if not abs_joined_path.startswith(abs_working_dir):
        return (f'Error: Cannot list "{directory}" is outside of the permitted working directory')

    if not os.path.isdir(abs_joined_path):
        return (f'Error: "{directory}" is not a directory')
    
    entries = os.listdir(abs_joined_path)

    strings = []
    for name in entries:
        full_path = os.path.join(abs_joined_path, name)
        is_dir = os.path.isdir(full_path)
        file_size = os.path.getsize(full_path)
        string = f'- {name}: file_size={file_size} bytes, is_dir={is_dir}'
        strings.append(string)
    
    result = "\n".join(strings)
    return result
