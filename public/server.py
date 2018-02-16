# -*- coding: utf-8 -*-

import os
import socket
import logging

logging.basicConfig(filename="info.log",
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")


class Server:
    def __init__(self, host, port, workers):
        self.address_pair = (host, int(port))
        self.workers = workers
        self.pid_workers = []

    def start(self):
        logging.info('server start')

        with socket.socket() as sock:
            sock.bind(self.address_pair)
            sock.listen()

            logging.info('parent pid: {}'.format(os.getpid()))

            for _ in range(self.workers):
                pid = os.fork()

                # fork в родительский процесс вернет PID дочернего процесса, а в дочернем процессе переменная
                # pid будет равна нулю

                if pid == 0:

                    logging.info('child pid: {}'.format(os.getpid()))
                    while True:
                        conn, adr = sock.accept()
                        with conn:
                            # while True:

                            logging.info('my pid is {}'.format(os.getpid()))
                            data = conn.recv(5)
                            print(data.decode("utf8"))

                else:
                    self.pid_workers.append(pid)
                    logging.info('parent pid: {} children pid: {}'.format(os.getpid(), pid))

            print(self.pid_workers)
            for pid in self.pid_workers:
                logging.info('kill workers: {} '.format(pid))
                os.waitpid(pid, 0)
