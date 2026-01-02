import os
from dotenv import load_dotenv

def get_file_content(working_directory, file_path):
    load_dotenv()
    max_chars = int(os.environ.get("MAX_FILE_READ_CHAR"))
    target_path = os.path.normpath(os.path.join(working_directory, file_path))
    #print(f"work: {os.path.abspath(working_directory)}")
    #print(f"target: {os.path.abspath(target_path)}")
    #print(f"path: {file_path}")

    if not os.path.exists(target_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        content = []
        item_info = ""
        with open(target_path, "r") as f:
            read_file = f.read(max_chars)
            item_info += f"Contents Size: {len(read_file)}"
            content.append(item_info)
            if f.read(1):
                item_info = f'...File "{file_path}" truncated at {max_chars} characters'
                content.append(item_info)
        return content
    
    except Exception as e:
        return f"Error: {e}"