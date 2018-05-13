# -*- coding: utf-8 -*-

import pytest

from bossfight.core.sharedGameData import GameStatus, SharedGameState


class TestSharedGameState:

    shared_game_state = SharedGameState()

    def test_shared_game_state_instantiation(self):
        assert self.shared_game_state.game_status == GameStatus.Paused
        paused_game_state = SharedGameState(game_status=GameStatus.Active)
        assert self.shared_game_state.game_status != paused_game_state.game_status
        paused_game_state.game_status = GameStatus.Paused
        assert self.shared_game_state == paused_game_state

    def test_shared_game_state_bytepacking(self):
        bytepack = self.shared_game_state.to_bytes()
        unpackedGameState = SharedGameState.from_bytes(bytepack)
        assert self.shared_game_state == unpackedGameState
        with pytest.raises(TypeError) as exception:
            SharedGameState.from_bytes('This is not a SharedGameState'.encode('utf-8'))
            assert str(exception.value) == 'Bytes could no be parsed into SharedGameState.'
