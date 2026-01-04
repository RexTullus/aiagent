import os
from dotenv import load_dotenv
from google.genai import types

def get_file_content(working_directory, file_path):
    load_dotenv()
    max_chars = int(os.environ.get("MAX_FILE_READ_CHAR"))

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
    common = os.path.commonpath([abs_working_dir, abs_file_path])
    
    if common != abs_working_dir:
        #print(abs_file_path)
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        item_info = ""
        with open(abs_file_path, "r") as f:
            read_file = f.read(max_chars)
            item_info = read_file
            if f.read(1):
                item_info += f'...File "{file_path}" truncated at {max_chars} characters'
        return item_info
    
    except Exception as e:
        return f"Error: {e}"
    

schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Reads the content of a given file in a specified directory relative to the working directory",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="file name with path where to read the file from, relative to the working directory (default is the working directory itself)",
            ),
        },
    required=["file_path"],
    ),
)