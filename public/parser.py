from constant.method import *


class Parser:

    def __init__(self, data):
        self.data = data
        [self.headers, self.body] = self._parse_request()

    def _parse_request(self):
        data = list(self.data.split('\r\n\r\n'))
        data_for_headers = data[0].split('\r\n')

        [self.method, self.uri, self.version_protocol] = data_for_headers[0].split(' ')

        return [
            {elem.split(': ')[0]: elem.split(': ')[1] for elem in data_for_headers[1:]},
            data[1] if self.method == POST else ''
        ]

    def get_response(self):
        return self
