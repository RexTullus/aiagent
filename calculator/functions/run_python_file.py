import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:    
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        common = os.path.commonpath([abs_working_dir, abs_file_path])

        if common != abs_working_dir:
            return f'Error:  Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        try:
            command = ["python", abs_file_path]
            if args:
                command.extend(args)
            result = subprocess.run(command, timeout=30, text=True, capture_output=True)

            result_return_code = result.returncode
            result_stdout = result.stdout
            result_stderr = result.stderr

            result_info = ""
            if result_return_code != 0:
                return "Process exited with code {result_return_code}"
            if not result_stdout: 
                result_stdout = "No output produced"
            if not result_stderr:
                result_stderr = "No output produced" 

            result_info = "STDOUT:" + result_stdout + "\n" + "STDERR:" + result_stderr
            return result_info

        except subprocess.CalledProcessError as e:
            print("An error occurred:", e)
            print("Return Code:", e.returncode)
            print("Output:", e.output)

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = types.FunctionDeclaration(
name="run_python_file",
description="Run a python file in a specified directory relative to the working directory",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="file name with path where to run the file, relative to the working directory (default is the working directory itself)",
            ),
        "args": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(  # Specify the items in the array
                type=types.Type.STRING,
                description="Arguments used for running the Python file, containing items of type STRING.",
                )
            ),
        },
    required=["file_path"],
    ),
)


