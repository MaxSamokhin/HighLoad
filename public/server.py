# -*- coding: utf-8 -*-

import os
import socket


class Server:
    def __init__(self, host, port, workers):
        self.address_pair = (host, int(port))
        self.workers = workers
        self.pid_workers = []

    def start(self):
        print('server start')
        with socket.socket() as sock:
            sock.bind(self.address_pair)
            sock.listen()

            print('parent pid: {}'.format(os.getpid()))

            for _ in range(self.workers):
                pid = os.fork()

                # fork в родительский процесс вернет PID дочернего процесса, а в дочернем процессе переменная
                # pid будет равна нулю

                if pid == 0:

                    print('child pid: {}'.format(os.getpid()))
                    while True:
                        conn, adr = sock.accept()
                        with conn:
                            # while True:
                            data = conn.recv(1024)
                            print(data.decode("utf8"))

                else:
                    self.pid_workers.append(pid)
                    print('parent pid: {} children pid: {}'.format(os.getpid(), pid))

            print(self.pid_workers)
            for pid in self.pid_workers:
                print('kill workers: {} '.format(pid))
                os.waitpid(pid, 0)
