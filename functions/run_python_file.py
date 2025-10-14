import os
import sys
import subprocess

def run_python_file(file_path, working_directory, args=None):
    if args is None:
        args = []

    wd_abs = os.path.abspath(working_directory)
    file_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not file_abs.startswith(wd_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(file_abs):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = [sys.executable, file_abs, *args]
        process_result = subprocess.run(
            command,
            cwd=wd_abs,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        stdout = process_result.stdout or ""
        stderr = process_result.stderr or ""
        return (stdout + stderr).rstrip()
    except Exception as e:
        return f"Error: executing Python file: {e}"