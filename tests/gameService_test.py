# -*- coding: utf-8 -*-

import socket
from bossfight.server.gameService import GameService
import bossfight.core.gameServiceProtocol as gsp

class TestGameService:

    server_address = ('localhost', 9998)
    server = GameService(server_address[0], server_address[1])
    mock_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    mock_client_socket.settimeout(1.0)

    def mock_client_request(self, datagram: bytes):
        self.mock_client_socket.sendto(datagram, self.server_address)

    def mock_client_recv(self, buffer_size=1024):
        return self.mock_client_socket.recv(buffer_size)

    def test_game_service_instantiation(self):
        assert self.server.shared_game_state == gsp.SharedGameState()
        assert self.server.RequestHandlerClass.__name__ == '_GameServiceRequestHandler'

    def test_game_service_request_handler(self):
        self.server.server_activate()
        self.mock_client_request(
            gsp.GameServicePackage(gsp.PackageType().GetSharedGameStateRequest).to_datagram()
        )
        self.server.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType().GameServiceResponse
        self.mock_client_request(bytes('Not a proper package', 'utf-8'))
        self.server.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType().GameServiceError and \
               response.body.error_type == gsp.ErrorType().UnpackError
        self.mock_client_request(
            gsp.GameServicePackage(gsp.PackageType().GameServiceResponse).to_datagram()
        )
        self.server.handle_request()
        response = gsp.GameServicePackage.from_datagram(self.mock_client_recv())
        assert response.header.package_type == gsp.PackageType().GameServiceError
        self.server.server_close()
