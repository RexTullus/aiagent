import os
from google.genai import types

def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common = os.path.commonpath([abs_working_dir, abs_file_path])
    
    if common != abs_working_dir:
        #print(abs_file_path)
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(abs_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
 
    os.makedirs(common,exist_ok=True)

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
name="write_file",
description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="file name with path where to the file to be written to, relative to the working directory (default is the working directory itself)",
            ),
        "content": types.Schema(
            type=types.Type.STRING,
            description="Content to be written to the file",
            ),
        },
    required=["file_path", "content"],
    ),
)
