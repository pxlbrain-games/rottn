# -*- coding: utf-8 -*-

import socketserver
#import threading
import bossfight.core.sharedGameData as sharedGameData
import bossfight.core.gameServiceProtocol as gsp

class UDPGameService(socketserver.ThreadingUDPServer):
    '''Threading UDP server that manages clients and processes requests.'''

    def __init__(self, server_address):
        super().__init__(server_address, _UDPGameServiceRequestHandler)
        self.sharedGameState = sharedGameData.SharedGameState()

class _UDPGameServiceRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Read out request
        gameServiceRequest = gsp.GameServicePackage.from_datagram(self.request[0])

        # Handle request and assign gameServiceResponse here
        if gameServiceRequest.header.package_type == gsp.PackageType.GetSharedGameStateRequest:
            gameServiceResponse = gsp.GameServicePackage(gsp.PackageType.GameServiceResponse, body=self.server.sharedGameState)
        else:
            gameServiceResponse = gsp.GameServicePackage(gsp.PackageType.GameServiceError)
        
        # Send response
        self.request[1].sendto(gameServiceResponse.to_datagram(), self.client_address)