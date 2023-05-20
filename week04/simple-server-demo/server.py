# python3 -m http.server

# from http.server import test, SimpleHTTPRequestHandler
#
# test(SimpleHTTPRequestHandler, port=8001)

#
from http.server import HTTPServer, SimpleHTTPRequestHandler

httpd = HTTPServer(('localhost', 8002), SimpleHTTPRequestHandler)
httpd.serve_forever()