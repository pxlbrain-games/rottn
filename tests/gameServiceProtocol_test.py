# -*- coding: utf-8 -*-

from bossfight.core.gameServiceProtocol import GameServicePackage, _GameServicePackageHeader, PackageType
from bossfight.core.sharedGameData import SharedGameState, GameStatus
import os
import pytest

class TestGameServicePackage:

    testGameServicePackage = GameServicePackage(PackageType.GetSharedGameStateRequest)

    def test_gameServicePackageInstance(self):
        assert self.testGameServicePackage.body == None
        otherGameServicePackage = GameServicePackage(PackageType.PostPlayerActionRequest)
        assert self.testGameServicePackage != otherGameServicePackage
        otherGameServicePackage.header.package_type = PackageType.GetSharedGameStateRequest
        assert self.testGameServicePackage == otherGameServicePackage
        otherGameServicePackage.body = SharedGameState()
        assert self.testGameServicePackage != otherGameServicePackage
        assert otherGameServicePackage.body.game_status == GameStatus.Paused

    def test_gameServicePackageHeaderBytepacking(self):
        bytepack = self.testGameServicePackage.header.to_bytes()
        unpackedHeader = _GameServicePackageHeader.from_bytes(bytepack)
        assert self.testGameServicePackage.header == unpackedHeader
        with pytest.raises(TypeError) as exception:
            _GameServicePackageHeader.from_bytes('This is not a header'.encode('utf-8'))
            assert str(exception.value) == 'Bytes could no be parsed into _GameServicePackageHeader.'

    def test_gameServicePackageWriteRead(self, tmpdir):
        mock_socket_path = os.path.join(tmpdir, 'mock.socket')
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            self.testGameServicePackage.write_to_datagram(mock_socket_wstream)
            mock_socket_wstream.write(bytes('some extra bytes', 'utf-8'))
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            receivedRequest = GameServicePackage.read_from_datagram(mock_socket_rstream)
            assert receivedRequest == self.testGameServicePackage
        otherGameServicePackage = GameServicePackage(PackageType.PostPlayerActionRequest, body=SharedGameState())
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            otherGameServicePackage.write_to_datagram(mock_socket_wstream)
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            receivedRequest = GameServicePackage.read_from_datagram(mock_socket_rstream)
            assert receivedRequest.body.game_status == GameStatus.Paused