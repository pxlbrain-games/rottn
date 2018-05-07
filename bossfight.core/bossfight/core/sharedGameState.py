# -*- coding: utf-8 -*-

from bossfight.core.gameServiceRequest import ISendable
from enum import IntEnum
import umsgpack

class GameStatus(IntEnum):
    Paused = 1
    Active = 2

class SharedGameState(ISendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Provides methods for sending and receiving SharedGameState objects via UDP sockets.
    '''

    def __init__(self, game_status=GameStatus.Active):
        self.game_status = game_status

    @staticmethod
    def _readDatagram(dgram:bytes):
        '''Decodes a a bytes object into a SharedGameState.'''
        receivedGameState = umsgpack.unpackb(dgram)
        try:
            return SharedGameState(game_status=receivedGameState['game_status'])
        except KeyError:
            raise TypeError('Read datagram could no be parsed to SharedGameState.')
    
    '''
    Overrides of object member functions:
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_status == other.game_status
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)