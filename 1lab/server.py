import os
import json

current_dir = os.getcwd()
file_structure = {}


def dir_s(start_path, structure):
    for a in os.listdir(start_path):
        # print(12, os.listdir(start_path))
        entry_path = os.path.join(start_path, a)
        # print(123, entry_path)
        if os.path.isdir(entry_path):
            print(f'Директория: {entry_path}')
            structure[a] = {}
            dir_s(entry_path, structure[a])
        else:
            print(f'Файл: {entry_path}')
            structure[a] = f'FILE{os.path.splitext(a)[1]}'


dir_s(current_dir, file_structure)

with open('result file.json', 'w') as json_file:
    json.dump(file_structure, json_file, indent=4)

with open('result file.json', 'r') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, indent=4))
