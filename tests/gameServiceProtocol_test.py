# -*- coding: utf-8 -*-

import pytest
from bossfight.core.gameServiceProtocol import \
    GameServicePackage, _GameServicePackageHeader, PackageType
from bossfight.core.sharedGameData import SharedGameState, GameStatus

class TestGameServicePackage:

    game_service_package = GameServicePackage(PackageType().GetSharedGameStateRequest)

    def test_game_service_package_instantiation(self):
        assert self.game_service_package.body is None
        other_game_service_package = GameServicePackage(PackageType().PostClientActivityRequest)
        assert self.game_service_package != other_game_service_package
        other_game_service_package.header.package_type = PackageType().GetSharedGameStateRequest
        assert self.game_service_package == other_game_service_package
        other_game_service_package.body = SharedGameState()
        assert self.game_service_package != other_game_service_package
        assert other_game_service_package.body.game_status == GameStatus().Paused

    def test_game_service_package_header_bytepacking(self):
        bytepack = self.game_service_package.header.to_bytes()
        unpacked_header = _GameServicePackageHeader.from_bytes(bytepack)
        assert self.game_service_package.header == unpacked_header
        with pytest.raises(TypeError) as exception:
            _GameServicePackageHeader.from_bytes('This is not a header'.encode('utf-8'))
            assert str(exception.value) == \
                'Bytes could no be parsed into _GameServicePackageHeader.'

    def test_game_service_package_datagrams(self):
        datagram = self.game_service_package.to_datagram()
        received_package = GameServicePackage.from_datagram(datagram)
        assert received_package == self.game_service_package
        other_game_service_package = GameServicePackage(
            PackageType().GetGameStateUpdateRequest,
            body=SharedGameState()
        )
        datagram = other_game_service_package.to_datagram()
        received_package = GameServicePackage.from_datagram(datagram)
        assert received_package.body.game_status == GameStatus().Paused
