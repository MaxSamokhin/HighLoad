from urllib.parse import urlparse, unquote


class Request:

    def __init__(self, request):
        self.headers, self.method, uri, self.version_protocol = self.__parse_request(request)
        self.host = self.headers.get('Host', '')
        self.url, self.path = self.__parse_url(uri)
        self.file_type = self.path.split('.')[-1]

    def __parse_request(self, req):
        data = req.split('\r\n\r\n')
        data_for_headers = data[0].split('\r\n')

        return [{elem.split(': ')[0]: elem.split(': ')[1]  # headers
                 for elem in data_for_headers[1:]}] + \
               data_for_headers[0].split(' ')  # method, uri, version_protocol

    def __parse_url(self, uri):
        full_url = '//' + self.host + uri
        full_url = urlparse(full_url)
        return full_url.geturl(), \
               unquote(full_url.path)  # unquote - Replace %xx escapes by their single-character equivalent.

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

    def get_file_type(self):
        return self.file_type

    def get_method(self):
        return self.method
