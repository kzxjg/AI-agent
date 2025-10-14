import os

def get_files_info(working_directory, directory="."):

    relative_path = os.path.join(working_directory, directory)

    if not os.path.abspath(relative_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(relative_path):
        return f'Error: "{directory}" is not a directory'
    
    try: 
            
        string_list = []
        for filename in os.listdir(relative_path):
            path = os.path.join(relative_path, filename)
            size = os.path.getsize(path)
            is_directory = os.path.isdir(path)
            full_string = f"- {filename}: file_size={size} bytes, is_dir={is_directory}"
            string_list.append(full_string)

        return '\n'.join(string_list)
    
    except OSError as e:
        return f'OS error: {e}'