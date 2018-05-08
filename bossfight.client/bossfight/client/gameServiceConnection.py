# -*- coding: utf-8 -*-

import socket
#import bossfight.core.sharedGameData as sharedGameData
import bossfight.core.gameServiceProtocol as gsp

class GameServiceConnection:
    def __init__(self, server_address):
        self.server_address = server_address
        self._client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._buffer_size = 1024
    
    def send_and_recv(self, package:gsp.GameServicePackage):
        '''
        Sends the package passed to it to the GameService and returns the servers response (as a GameServicePackage).
        '''
        self._client_socket.sendto(package.to_datagram(), self.server_address)
        return gsp.GameServicePackage.from_datagram(self._client_socket.recv(self._buffer_size))