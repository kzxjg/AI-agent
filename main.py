import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types 
import argparse
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


functions_by_name = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}



parser = argparse.ArgumentParser()
parser.add_argument("prompt", nargs="+", help="Prompt for the model")  # captures words
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

verbose = args.verbose


prompt = " ".join(args.prompt) 



load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Read and return the contents of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file path to the file, relative to the working directory.",
                ),
            },
        required=["file_path"],
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the python file that is in the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required = ['file_path'],
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to the file in the specified file path.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Write or overwrite a file, constrained to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description = 'Content for the file to replace with.'
            )
        },
    
        required = ['file_path', 'content'],
    ),
)


available_functions = types.Tool(
 
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    args = function_call_part.args.copy()
    args["working_directory"] = "./calculator"


    print(f"- Calling function: {function_name}")


    func = functions_by_name.get(function_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

message_list = []

message_list.append(
    types.Content(
        role="user",
        parts=[types.Part(text = prompt)]
    )
)


for i in range(20):

    try:

        response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = message_list,
            config = config
        )

        if response.candidates:
            message_list.append(response.candidates[0].content)

        if response.candidates and response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
            func_call = response.candidates[0].content.parts[0].function_call
            tool_content = call_function(func_call, verbose=verbose)
            user_content= types.Content(
                role = 'user',
                parts = tool_content.parts
            )

            message_list.append(user_content)

            func_resp = tool_content.parts[0].function_response.response
            
            result_str = func_resp.get("result", "")
            if verbose:
                print(f"-> {result_str}")
            
        if response.text:
            print(response.text)
            break

        
    except Exception as e:
        raise print(f'Error: {e}')





