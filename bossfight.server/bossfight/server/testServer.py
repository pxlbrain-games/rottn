# -*- coding: utf-8 -*-

import socketserver
#import threading
from bossfight.core.sharedGameState import SharedGameState, GameStatus

class UDPGameService(socketserver.ThreadingUDPServer):
    '''Threading UDP server that provides clients with the shared game state.'''

    def __init__(self, server_address):
        super().__init__(server_address, _UDPGameServiceRequestHandler)
        self.sharedGameState = SharedGameState()

class _UDPGameServiceRequestHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        datagram = str(self.rfile.readline(), 'utf-8')
        self.wfile.write(('Hello Client! You sent: ' + datagram).encode('utf-8'))