# -*- coding: utf-8 -*-

from bossfight.server.gameService import UDPGameService
from bossfight.client.gameServiceConnection import UDPGameServiceConnection
import bossfight.core.gameServiceProtocol as gsp
import pytest

class TestGameService:

    server_address = ('localhost', 9998)
    testServer = UDPGameService(server_address)
    testClient = UDPGameServiceConnection(server_address)

    def test_UDPGameServiceInstance(self):
        assert self.testServer.sharedGameState == gsp.SharedGameState()
        assert self.testServer.RequestHandlerClass.__name__ == '_UDPGameServiceRequestHandler'
    
    def test_UDPGameServiceConnectionInstance(self):
        assert self.testClient._buffer_size == 1024
    
    def test_GameServicePackageTransmission(self):
        #with pytest.raises():
        #    self.testClient.send_and_recv(gsp.GameServicePackage(gsp.PackageType.GetSharedGameStateRequest))
        self.testServer.serve_forever()
        response = self.testClient.send_and_recv(gsp.GameServicePackage(gsp.PackageType.GetGameStateUpdateRequest))
        assert response.header.package_type == gsp.PackageType.GameServiceError
        self.testServer.shutdown()