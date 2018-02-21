from server import Server
from constant.server import *
from logger import Logger


def main():
    Logger.info('Main')
    server = Server(HOST, PORT, WORKERS, SIZE_QUEUE, CHUNK)
    server.start()


if __name__ == '__main__':
    main()
