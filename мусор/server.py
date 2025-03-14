import os
import json
import socket

port = 19200
host = 'localhost'
root_dir = os.getcwd()
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


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((host, port))
    print(f"Сервер запущен на {host}:{port}")

except Exception:
    print('Error host')

server_socket.listen(1)
while True:
    conn, addr = server_socket.accept()
    print(f"Подключено к {addr}")

    command = conn.recv(2048).decode()
    print('ДАТА СЕРВЕР = ', command)
    try:
        if command.startswith("dirs"):
            file_structure.clear()
            dir_s(root_dir, file_structure)
            with open('../1lab/result_file.json', 'w') as json_file:
                json.dump(file_structure, json_file, indent=4)
            conn.sendall(json.dumps(file_structure).encode())
            conn.sendall('\n'.encode())
            conn.sendall('Save in JSON file'.encode())
            conn.sendall('\n'.encode())
            print(command)
            #command = conn.recv(2048).decode()


        elif command.startswith("c"):
            conn.sendall('command change received'.encode())
            new_directory = command.split(" ")[1]
            if os.path.isdir(new_directory):
                root_dir = new_directory
                conn.sendall(f"Директория успешно изменена на: {root_dir}".encode())

            else:
                conn.sendall(b"Error  Invalid direction")

        elif command.startswith('ways'):
            print('зашел в в')
            print(len(root_dir.encode()))
            conn.sendall(len(root_dir.encode()))
            conn.sendall(f'data = {command}'.encode())
            ##data = conn.recv(2048).decode()
            command = None

        elif command.startswith('exit'):
            conn.close()
            server_socket.close()
            break

    except Exception:
        print('Bad command')
