from server import Server
from constant import *


def main():
    server = Server(HOST, PORT, WORKERS)
    server.start()


if __name__ == '__main__':
    main()
