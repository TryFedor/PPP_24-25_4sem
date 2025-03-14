import socket
import struct


def main():
    address = ('localhost', 19200)
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(address)
    try:
        while True:
            cmd = input("Введите команду: \n"
                        " ways (текущая директория), \n"
                        "dirs (все файлы и подфайлы в текущей директории), \n"
                        "change <NEW WAY>, \n "
                        "exit (выход из клиента) \n")
            if cmd.lower() == "exit":
                socket_client.send(b'exit')
                break
            else:
                socket_client.send(cmd.encode())
                length = socket_client.recv(4)
                response_size = struct.unpack('!I', length)[0]
                response_data = b""
                while len(response_data) < response_size:
                    part = socket_client.recv(1024)
                    if not part:
                        break
                    response_data += part
                print("Ответ от сервера:")
                print(response_data.decode())

    except Exception as error:
        print(f"Ошибка: {error}")
    finally:
        socket_client.close()


if __name__ == "__main__":
    main()
