# -*- coding: utf-8 -*-

from bossfight.core.gameServiceRequest import GameServiceRequest, _GameServiceRequestHeader, RequestType
from bossfight.core.sharedGameData import SharedGameState, GameStatus
import os

class TestGameServiceRequest:

    testGameServiceRequest = GameServiceRequest(RequestType.GetSharedGameState)

    def test_gameServiceRequestInstance(self):
        assert self.testGameServiceRequest.body == None
        otherGameServiceRequest = GameServiceRequest(RequestType.PostPlayerAction)
        assert self.testGameServiceRequest != otherGameServiceRequest
        otherGameServiceRequest.header.request_type = RequestType.GetSharedGameState
        assert self.testGameServiceRequest == otherGameServiceRequest
        otherGameServiceRequest.body = SharedGameState()
        assert self.testGameServiceRequest != otherGameServiceRequest
        assert otherGameServiceRequest.body.game_status == GameStatus.Paused

    def test_gameServiceRequestHeaderBytepacking(self):
        bytepack = self.testGameServiceRequest.header.to_bytes()
        unpackedHeader = _GameServiceRequestHeader.from_bytes(bytepack)
        assert self.testGameServiceRequest.header == unpackedHeader

    def test_gameServiceRequestWriteRead(self, tmpdir):
        mock_socket_path = os.path.join(tmpdir, 'mock.socket')
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            self.testGameServiceRequest.write_to_datagram(mock_socket_wstream)
            mock_socket_wstream.write(bytes('some extra bytes', 'utf-8'))
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            receivedRequest = GameServiceRequest.read_from_datagram(mock_socket_rstream)
            assert receivedRequest == self.testGameServiceRequest
        otherGameServiceRequest = GameServiceRequest(RequestType.PostPlayerAction, body=SharedGameState())
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            otherGameServiceRequest.write_to_datagram(mock_socket_wstream)
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            receivedRequest = GameServiceRequest.read_from_datagram(mock_socket_rstream)
            assert receivedRequest.body.game_status == GameStatus.Paused