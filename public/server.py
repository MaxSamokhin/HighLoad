# -*- coding: utf-8 -*-

import os
import socket
from logger import Logger
from request import Request
from response import Response


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

                            if len(request.strip()) == 0:  # empty  request
                                conn.close()
                                continue

                            Logger.info(request.decode('utf8'))

                            # print('Request: {}'.format(request.decode()))

                            pars_request = Request(request.decode())
                            response = Response(pars_request, root_dir='/home/max/max/highload/HighLoad')

                            print(response.get_response().decode())

                            conn.sendall(response.get_response())

                else:

                    self.pid_workers.append(pid)
                    Logger.info('Parent pid: {} Children pid: {}'.format(os.getpid(), pid))

            Logger.info("Pid workers: {}".format(self.pid_workers))

            for pid in self.pid_workers:
                os.waitpid(pid, 0)
