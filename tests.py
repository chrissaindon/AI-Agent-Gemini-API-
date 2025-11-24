from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

return_format = "Result for current file:"


print(return_format)
print(get_file_content("calculator", "main.py"))

print(return_format)
print(get_file_content("calculator", "pkg/calculator.py"))

print(return_format)
print(get_file_content("calculator", "/bin/cat"))

print(return_format)
print(get_file_content("calculator", "pkg/does_not_exist.py"))








