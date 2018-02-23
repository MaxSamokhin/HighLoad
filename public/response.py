import os
from datetime import datetime

from constant.request_method import GET, HEAD, POST
from constant.content_type import CONTENT_TYPE
from constant.status_code import OK, METHOD_NOT_ALLOWED, NOT_FOUND, RESPONSE_STATUS
from constant.http import HTTP_VERSION, HTTP_DATE
from constant.server import SERVER_NAME


class Response:

    def __init__(self, request, root_dir):
        self.code = None
        self.content = None
        self.content_length = None
        self.content_type = CONTENT_TYPE.get(request.get_file_type(), '')

        self.__create_response(request, root_dir)

    def __create_response(self, req, root_dir):
        filename = os.path.normpath(root_dir + '/' + req.get_path())

        with open(filename, 'rb') as f:
            self.content = f.read() if req.get_method() == GET else b''
            self.content_length = len(self.content)
            self.code = OK

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
        )
