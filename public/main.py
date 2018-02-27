import argparse
from server import Server
from constant.server import *
from logger import Logger
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', default=ROOT_DIR, help='ROOT DIR')
    parser.add_argument('-c', default=COUNT_CPU, help='CPU COUNT')

    argv = parser.parse_args()
    Logger.info('\ncount cpu: {} \nroot dir: {} \n'.format(argv.c, argv.r))

    if not os.path.exists(argv.r):
        Logger.info('Error: can`t find root directory: {}'.format(argv.r))
        sys.exit()

    server = Server(HOST, PORT, int(argv.c), SIZE_QUEUE, CHUNK, argv.r)
    server.start()


if __name__ == '__main__':
    main()
