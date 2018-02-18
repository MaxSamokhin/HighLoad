# -*- coding: utf-8 -*-

import os
import socket
from logger import Logger


class Server:
    def __init__(self, host, port, workers, size_queue, chunk):
        Logger.info('Init server param')
        self.address_pair = (host, int(port))
        self.workers = workers
        self.pid_workers = []
        self.size_queue = size_queue
        self.chunk = chunk

    def start(self):
        Logger.info('Server start')
        with socket.socket() as sock:

            sock.bind(self.address_pair)
            sock.listen(self.size_queue)
            Logger.info('Parent pid: {}'.format(os.getpid()))

            for _ in range(self.workers):
                pid = os.fork()

                # fork в родительский процесс вернет PID дочернего процесса,
                # а в дочернем процессе переменная pid будет равна нулю

                if pid == 0:
                    Logger.info('Child pid: {}'.format(os.getpid()))

                    while True:
                        conn, adr = sock.accept()
                        with conn:

                            request = conn.recv(self.chunk)
                            Logger.info(request.decode('utf8'))
                            conn.sendall('your data: {}'.format(request.decode('utf8')).encode('utf8'))

                else:

                    self.pid_workers.append(pid)
                    Logger.info('Parent pid: {} Children pid: {}'.format(os.getpid(), pid))

            Logger.info("Pid workers: {}".format(self.pid_workers))

            for pid in self.pid_workers:
                Logger.info('param pam pam {} '.format(pid))
                os.waitpid(pid, 0)
