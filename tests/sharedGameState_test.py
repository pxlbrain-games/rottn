# -*- coding: utf-8 -*-

from bossfight.core.sharedGameState import SharedGameState, GameStatus
import pytest
import os

class TestSharedGameState(object):

    testSharedGameState = SharedGameState()

    def test_sharedGameStateInstance(self):
        assert self.testSharedGameState.game_status == GameStatus.Active
        pausedGameState = SharedGameState(game_status=GameStatus.Paused)
        assert self.testSharedGameState.game_status != pausedGameState.game_status

    def test_sharedGameStateDatagram(self, tmpdir):
        mock_socket_path = os.path.join(tmpdir, 'mock_socket')
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            self.testSharedGameState._writeDatagram(mock_socket_wstream)
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            receivedGameState = SharedGameState._readDatagram(mock_socket_rstream.read())
            assert self.testSharedGameState == receivedGameState
        with open(mock_socket_path, mode='wb') as mock_socket_wstream:
            mock_socket_wstream.write('This is not a SharedGameState'.encode('utf-8'))
        with open(mock_socket_path, mode='rb') as mock_socket_rstream:
            with pytest.raises(TypeError) as exception:
                SharedGameState._readDatagram(mock_socket_rstream.read())
                assert str(exception.value) == 'Read datagram could no be parsed to SharedGameState.'