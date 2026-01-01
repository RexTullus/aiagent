import os

def get_file_content(working_directory, file_path):
    
    f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
