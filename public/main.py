#!/usr/bin/env python

import argparse
from server import Server
from constant.server import *
from logger import Logger
import os
import sys
from parser_config import load_config


def main():

    if False:
        config = load_config()
        port = int(config['listen'])
        count_cpu = int(config['cpu_limit'])
        document_root = config['document_root']
    else:
        port = PORT
        count_cpu = COUNT_CPU
        document_root = ROOT_DIR

    Logger.info('\nport: {}\ncount cpu: {} \nroot dir: {} \n'.format(port, count_cpu, document_root))

    if not os.path.exists(document_root):
        Logger.info('Error: can`t find root directory: {}'.format(document_root))
        sys.exit()

    server = Server(HOST, port, count_cpu, SIZE_QUEUE, CHUNK, document_root)
    server.start()


if __name__ == '__main__':
    main()
