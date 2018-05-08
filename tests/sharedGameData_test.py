# -*- coding: utf-8 -*-

from bossfight.core.sharedGameData import SharedGameState, GameStatus
import pytest

class TestSharedGameState:

    testSharedGameState = SharedGameState()

    def test_sharedGameStateInstance(self):
        assert self.testSharedGameState.game_status == GameStatus.Paused
        pausedGameState = SharedGameState(game_status=GameStatus.Active)
        assert self.testSharedGameState.game_status != pausedGameState.game_status
        pausedGameState.game_status = GameStatus.Paused
        assert self.testSharedGameState == pausedGameState

    def test_sharedGameStateBytepacking(self):
        bytepack = self.testSharedGameState.to_bytes()
        unpackedGameState = SharedGameState.from_bytes(bytepack)
        assert self.testSharedGameState == unpackedGameState
        with pytest.raises(TypeError) as exception:
            SharedGameState.from_bytes('This is not a SharedGameState'.encode('utf-8'))
            assert str(exception.value) == 'Bytes could no be parsed into SharedGameState.'