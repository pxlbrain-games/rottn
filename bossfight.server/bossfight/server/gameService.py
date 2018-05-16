# -*- coding: utf-8 -*-
'''
This module defines the *GameService* class, a server that can handle requests from
a client's *GameServiceConnection* object.
'''

import socketserver
from umsgpack import InsufficientDataException
import netifaces
import bossfight.core.sharedGameData as sharedGameData
import bossfight.core.gameServiceProtocol as gsp

class GameService(socketserver.ThreadingUDPServer):
    '''
    Threading UDP server that manages clients and processes requests.

    Call *serve_forever*() in a seperate thread for the server to start handling requests from
    *GameServiceConnection*s. Call *shutdown*() to stop it.
    '''

    def __init__(self, ip_address: str, port: int):
        super().__init__((ip_address, port), _GameServiceRequestHandler)
        self.shared_game_state = sharedGameData.SharedGameState()

    def get_address(self):
        '''
        Returns a tuple *(ip_address: str, port: int)* that represents the servers address.
        '''
        return self.socket.getsockname()

    @staticmethod
    def get_available_ip_addresses():
        '''
        Returns a list of all available IP addresses that the server can be bound to.
        Keep in mind that `127.0.0.1` is only suitable for local servers.
        '''
        addresses = []
        for interface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(interface):
                for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                    addresses.append(link['addr'])
        return addresses

class _GameServiceRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Read out request
        try:
            request = gsp.GameServicePackage.from_datagram(self.request[0])
        except (InsufficientDataException, TypeError):
            # if unpacking request failed send back error message and exit handle function
            response = gsp.GameServicePackage(
                package_type=gsp.PackageType.GameServiceError,
                body=gsp.ErrorMessage(
                    gsp.ErrorType.UnpackError,
                    'Server responded: Byte error.'
                )
            )
            self.request[1].sendto(response.to_datagram(), self.client_address)
            return

        # Handle request and assign response here
        if request.header.package_type == gsp.PackageType.GetSharedGameStateRequest or \
           request.header.package_type == gsp.PackageType.GetGameStateUpdateRequest:
            # respond by sending back the shared game state
            response = gsp.GameServicePackage(
                package_type=gsp.PackageType.GameServiceResponse,
                body=self.server.shared_game_state
            )
        else:
            # if none of the above were a match the request was invalid
            response = gsp.GameServicePackage(
                package_type=gsp.PackageType.GameServiceError,
                body=gsp.ErrorMessage(
                    gsp.ErrorType.RequestInvalid,
                    'Server responded: Request invalid.'
                )
            )

        # Send response
        self.request[1].sendto(response.to_datagram(), self.client_address)
