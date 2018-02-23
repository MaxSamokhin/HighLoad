from urllib.parse import urlparse, unquote
from constant.content_type import CONTENT_TYPE


class Request:

    def __init__(self, request):
        self.headers, method, uri, self.version_protocol = self.__parse_request(request)
        self.host = self.headers.get('Host', '')
        self.url, self.path = self.__parse_url(uri)
        self.content_type = CONTENT_TYPE.get(self.path.split('.')[-1], '')

    def __parse_request(self, request):
        data = request.split('\r\n\r\n')
        data_for_headers = data[0].split('\r\n')

        return [{elem.split(': ')[0]: elem.split(': ')[1]  # headers
                 for elem in data_for_headers[1:]}] + \
               data_for_headers[0].split(' ')  # method, uri, version_protocol

    def __parse_url(self, uri):
        full_url = '//' + self.host + uri
        full_url = urlparse(full_url)
        return full_url.geturl(), unquote(full_url.path)

    def get_headers(self):
        return self.headers

    def get_version_protocol(self):
        return self.version_protocol

    def get_host(self):
        return self.host

    def get_url(self):
        return self.url

    def get_path(self):
        return self.path

    def get_content_type(self):
        return self.content_type
