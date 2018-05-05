# -*- coding: utf-8 -*-

import socketserver
#import threading

class TestUDPServer(socketserver.ThreadingUDPServer):
    def __init__(self, server_address):
        super().__init__(server_address, _TestUDPServerRequestHandler)


class _TestUDPServerRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        datagram = str(self.rfile.readline(), 'utf-8')
        self.wfile.write(('Hello Client! You sent: ' + datagram).encode('utf-8'))