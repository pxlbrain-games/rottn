# -*- coding: utf-8 -*-

from bossfight.core.gameServiceProtocol import GameServicePackage, _GameServicePackageHeader, PackageType
from bossfight.core.sharedGameData import SharedGameState, GameStatus
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

    def test_gameServicePackageWriteRead(self):
        datagram = self.testGameServicePackage.to_datagram()
        receivedPackage = GameServicePackage.from_datagram(datagram)
        assert receivedPackage == self.testGameServicePackage
        otherGameServicePackage = GameServicePackage(PackageType.GetGameStateUpdateRequest, body=SharedGameState())
        datagram = otherGameServicePackage.to_datagram()
        receivedPackage = GameServicePackage.from_datagram(datagram)
        assert receivedPackage.body.game_status == GameStatus.Paused