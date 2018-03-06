# -*- coding: utf-8 -*-

import os
import socket
from logger import Logger
from request import Request
from response import Response


class Server:
    def __init__(self, host, port, count_cpu, size_queue, chunk, root_dir):
        # Logger.info('Init server param')
        self.address_pair = (host, int(port))
        self.count_cpu = count_cpu
        self.pid_workers = []
        self.size_queue = size_queue
        self.chunk = chunk
        self.root_dir = root_dir

    def start(self):
        Logger.info('Server start')
        with socket.socket() as sock:
            # чтобы несколько приложений могли «слушать» сокет
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            sock.bind(self.address_pair)
            sock.listen(self.size_queue)
            Logger.info('Parent pid: {}'.format(os.getpid()))

            for _ in range(self.count_cpu):
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

                            pars_request = Request(request.decode())
                            response = Response(pars_request, root_dir=self.root_dir)
                            conn.sendall(response.get_response())

                else:

                    self.pid_workers.append(pid)
                    Logger.info('Parent pid: {} Children pid: {}'.format(os.getpid(), pid))

            for pid in self.pid_workers:
                os.waitpid(pid, 0)
