import json
import os
import socket
import struct
from termcolor import colored, cprint


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


'''
def print_tree(directory, prefix=""):
    ans = ''
    print(directory.items())
    for name, content in directory.items():
        if isinstance(content, dict):
            ans += prefix + "├── " + name
            ans += '\n'
            print_tree(content, prefix + "│   ")
        else:
            ans += prefix + "├── " + name
            ans += '\n'
    print(123, ans)
    return ans
'''


def print_tree(data, indent=0, color='white'):
    for key, value in data.items():
        print(colored(' ' * indent + key, color=color))
        if isinstance(value, dict):
            print_tree(value, indent + 4, color='light_grey')
            #print('\n')


#with open('result_file.json', 'r') as file:
#    json_data = json.load(file)

#print_tree(json_data)


def optimize(client_socket):
    response = ''
    flag_dirs = False
    global root_dir
    while True:

        command = client_socket.recv(1024).decode()
        if not command:
            break

        if command.startswith("change"):
            new_directory = command.split(" ", 1)[1]
            if os.path.isdir(new_directory):
                root_dir = new_directory
                response = colored("Директория изменена", 'green')
            else:
                response = colored("Ошибка. Директория не изменена", 'red')

        elif command.startswith("ways"):
            response = root_dir

        elif command == "exit":
            print(colored("КЛИЕНТ ЗАКРУГЛИЛСЯ ()", 'red',   attrs=['blink']))
            client_socket.close()
            exit()
            # break

        elif command == 'draw':

            if flag_dirs:
                with open('result_file.json', 'r') as file:
                    data = json.load(file)
                print_tree(data)

            else:
                response = colored('Ошибка! Сначала напиши $ dirs', 'red')


        elif command == 'dirs':
            response = colored('Файл готов result_file.json готов', 'light_green')
            file_structure.clear()
            dir_s(root_dir, file_structure)
            with open('result_file.json', 'w') as json_file:
                json.dump(file_structure, json_file, indent=4)
            flag_dirs = True

        response_bytes = response.encode()
        response_length = struct.pack('!I', len(response_bytes))
        client_socket.send(response_length + response_bytes)

    client_socket.close()


def start():
    server_address = ('localhost', 19200)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print("Сервер запущен. ПОРТ - 19200")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")
        optimize(client_socket)


if __name__ == "__main__":
    start()
