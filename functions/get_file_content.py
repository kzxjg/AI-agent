import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):

    relative_path = os.path.join(working_directory, file_path)
    if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{relative_path}" as it is outside the permitted working directory'
    
    
    if not os.path.isfile(relative_path):
        return f'Error: File not found or is not a regular file: "{relative_path}"'
    


    try: 

        with open(relative_path, 'r') as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string + f'[...File "{relative_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string


    except Exception as e:
        return f'Error: {e}'
          