# -*- coding: utf-8 -*-

from bossfight.server.gameService import GameService
import bossfight.core.gameServiceProtocol as gsp
import socket
import pytest

class TestGameService:

    server_address = ('localhost', 9998)
    testServer = GameService(server_address)
    mock_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    mock_client_socket.settimeout(1.0)

    def mock_client_request(self, datagram:bytes):
        self.mock_client_socket.sendto(datagram, self.server_address)
    
    def mock_client_recv(self, buffer_size=1024):
        return self.mock_client_socket.recv(buffer_size)
        
    def test_UDPGameServiceInstance(self):
        assert self.testServer.sharedGameState == gsp.SharedGameState()
        assert self.testServer.RequestHandlerClass.__name__ == '_GameServiceRequestHandler'
    
    def test_GameServicePackageTransmission(self):
        self.testServer.server_activate()
        self.mock_client_request(gsp.GameServicePackage(gsp.PackageType.GetSharedGameStateRequest).to_datagram())
        self.testServer.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType.GameServiceResponse
        self.mock_client_request(bytes('Not a proper package', 'utf-8'))
        self.testServer.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType.GameServiceError and \
               response.body.error_type == gsp.ErrorType.UnpackError
        self.mock_client_request(gsp.GameServicePackage(gsp.PackageType.GameServiceResponse).to_datagram())
        self.testServer.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType.GameServiceError
        self.testServer.server_close()
    