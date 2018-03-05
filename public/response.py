# -*- coding: utf-8 -*-

import os
from datetime import datetime
from logger import Logger

from constant.request_method import GET, HEAD, POST
from constant.content_type import CONTENT_TYPE
from constant.status_code import OK, METHOD_NOT_ALLOWED, NOT_FOUND, RESPONSE_STATUS, FORBIDDEN
from constant.http import HTTP_VERSION, HTTP_DATE, MAIN_PAGE
from constant.server import SERVER_NAME


class Response:

    def __init__(self, request, root_dir):
        self.code = None
        self.content = None
        self.content_length = None
        self.content_type = CONTENT_TYPE.get(request.get_file_type(), '')

        self.__create_response(request, root_dir)

    def __create_response(self, req, root_dir):
        if req.get_method() not in [GET, HEAD]:
            self.code = METHOD_NOT_ALLOWED
            return

        filename = os.path.normpath(root_dir + req.get_path())
        self.code = NOT_FOUND  # не существует файла или дирректории или в пути нет root

        # Logger.info('\n\nroot_dir: {} \n'
        #             'path: {} \n'
        #             'filename: {} \n'
        #             'os.path.commonprefix([filename, root_dir]) == root_dir : {} \n'
        #             'os.path.isfile(os.path.join(filename, MAIN_PAGE)) : {} \n'.format(
        #     root_dir,
        #     req.get_path(),
        #     filename,
        #     os.path.commonprefix([filename, root_dir]) == root_dir,
        #     os.path.isfile(os.path.join(filename, MAIN_PAGE)),
        #     os.path.exists(os.path.join(filename))
        # ))

        if os.path.commonprefix([filename, root_dir]) != root_dir:  # в пути нет root - /etc/passwd
            return

        if os.path.isfile(os.path.join(filename, MAIN_PAGE)):
            filename = os.path.join(filename, MAIN_PAGE)  # в дирректории берем MAIN_PAGE
        elif os.path.exists(os.path.join(filename)):  # существуют файл или дирректория
            self.code = FORBIDDEN

        try:
            with open(filename, 'rb') as f:
                content = f.read()
                self.content = content if req.get_method() == GET else b''
                self.content_length = len(content)
                self.code = OK
        except IOError as e:
            Logger.info('Error  -  file not found:    {}'.format(e.filename))

    def get_response(self):
        if self.code == OK:
            return self.__ok()

        return self.__error()

    def __ok(self):
        return (
                   'HTTP/{version} {status}\r\n'
                   'Server: {server}\r\n'
                   'Date: {date}\r\n'
                   'Connection: Close\r\n'
                   'Content-Length: {content_length}\r\n'
                   'Content-Type: {content_type}\r\n\r\n'
               ).format(
            version=HTTP_VERSION,
            status=RESPONSE_STATUS.get(self.code),
            server=SERVER_NAME,
            date=datetime.utcnow().strftime(HTTP_DATE),
            content_length=self.content_length,
            content_type=self.content_type
        ).encode() + self.content

    def __error(self):
        return (
            'HTTP/{version} {status}\r\n'
            'Server: {server}\r\n'
            'Date: {date}\r\n'
            'Connection: Close\r\n\r\n'
        ).format(
            version=HTTP_VERSION,
            status=RESPONSE_STATUS.get(self.code),
            server=SERVER_NAME,
            date=datetime.utcnow().strftime(HTTP_DATE),
        ).encode()
