import argparse
from server import Server
from constant.server import *
from logger import Logger
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', default=ROOT_DIR, help='ROOT DIR')
    argv = parser.parse_args()

    if not os.path.exists(argv.r):
        Logger.info('Error: can`t find root directory: {}'.format(argv.r))
        sys.exit()

    server = Server(HOST, PORT, COUNT_CPU, SIZE_QUEUE, CHUNK, argv.r)
    server.start()


if __name__ == '__main__':
    main()
