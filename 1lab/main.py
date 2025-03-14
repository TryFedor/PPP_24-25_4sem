import os
from threading import Thread
from server import start
import client


def main():
    try:
        client.main()
    except Exception as e:
        print(f'Ошибка {e} при запуске клиента')

def start_server():
    try:
        start()
    except Exception as e:
        print(f'Ошибка {e} при запуске сервера')


if __name__ == '__main__':
    Thread(target=main).start()
    Thread(target=start_server).start()