from urllib.parse import urlparse, unquote, parse_qs


class Parser:

    def __init__(self, request):
        self.headers, method, uri, self.version_protocol = self._parse_request(request)
        self.host = self.headers.get('Host', '')
        self.url, self.path = self.parse_url(uri)

    @staticmethod
    def _parse_request(request):
        data = request.split('\r\n\r\n')
        data_for_headers = data[0].split('\r\n')

        return [{elem.split(': ')[0]: elem.split(': ')[1]  # headers
                 for elem in data_for_headers[1:]}] + \
               data_for_headers[0].split(' ')  # method, uri, version_protocol

    def parse_url(self, uri):
        full_url = '//' + self.host + uri
        full_url = urlparse(full_url)
        return full_url.geturl(), unquote(full_url.path)

    def get_response(self):
        return self