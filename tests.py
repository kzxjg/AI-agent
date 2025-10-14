from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

print(run_python_file("main.py", "calculator"))
print(run_python_file("main.py", "calculator", ["3 + 5"]))
print(run_python_file("tests.py", "calculator"))
print(run_python_file("../main.py", "calculator"))
print(run_python_file("nonexistent.py", "calculator"))
