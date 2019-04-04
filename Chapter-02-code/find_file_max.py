import os

max_size = 0
for dir_path, dir_names, file_names in os.walk(r'd:\py\peixun\python-dev'):
    for file_name in file_names:
        path = os.path.join(dir_path, file_name)
        file_size = os.path.getsize(path)
        if file_size > max_size:
            max_size = file_size
            max_file = path

print(max_file, max_size)
