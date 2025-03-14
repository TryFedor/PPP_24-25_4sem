import socket
import struct


def main():
    server_address = ('localhost', 19200)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(server_address)
        print("Соединение с сервером установлено.")

        while True:
            command = input("Введите команду (dir, change или exit): ")
            data = ''
            command_b = command.encode()
            if command.lower() == 'c':
                new_path = input("Введите новый путь к директории: ")
                # struct.pack('!I', len(command_b))
                # client_socket.send(command_b)
                client_socket.send(b'c ')
                client_socket.send(new_path.encode('utf-8'))
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                #data = client_socket.recv(4096).decode('utf-8')
                print("Структура директории:")
                print(data)


            elif command.lower() == 'dir':
                client_socket.send(b'd ')
                #struct.pack('!I', len(command_b))
                #client_socket.send(command_b)
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                print("Структура директории:")
                print(data)

            elif command.lower() == 'way':
                client_socket.send(b'w ')
                print('way command client')
                by = int(client_socket.recv(4).decode())
                data = client_socket.recv(by).decode()
                print(data)
                #while True:
                #    data = client_socket.recv(1024).decode()
                #    print('while ', data)
                #    if not data:
                #        break
                print("Текущий путь:")
                print(data)
            elif command.lower() == 'exit':

                print("Закрытие клиента.")
                break
            else:
                print("Неверная команда.")

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()