#!/usr/bin/env python

import argparse
from server import Server
from constant.server import *
# from logger import Logger
import os
import sys
from parser_config import load_config


def main():
    config = load_config()

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-r', default=ROOT_DIR, help='ROOT DIR')
    # parser.add_argument('-c', default=COUNT_CPU, help='CPU COUNT')
    #
    # argv = parser.parse_args()
    # Logger.info('\ncount cpu: {} \nroot dir: {} \n'.format(argv.c, argv.r))

    if not os.path.exists(config['document_root']):
        # Logger.info('Error: can`t find root directory: {}'.format(argv.r))
        sys.exit()

    print('{} {} {}'.format(int(config['cpu_limit']), int(config['listen']), config['document_root']))

    server = Server(HOST, int(config['listen']), int(config['cpu_limit']), SIZE_QUEUE, CHUNK, config['document_root'])
    server.start()


if __name__ == '__main__':
    main()
