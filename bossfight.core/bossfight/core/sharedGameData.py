# -*- coding: utf-8 -*-

from enum import IntEnum
import umsgpack

class ISendable:
    '''
    Interface for objects that are supposed to be sendable as part of a server request or response.
    Inheriting classes must implement the static method `from_bytes(bytepack)` and possibly `to_bytes(self)`.
    `from_bytes(bytepack)` should return an instance of the inheriting class, if the argument was generated with `to_bytes()`.
    '''

    def to_bytes(self):
        '''
        Packs and return a small a binary representation of self.
        Override this, if simple __dict__ serialization is insufficient.
        '''
        return umsgpack.packb(self.__dict__)

    @staticmethod
    def from_bytes(bytepack):
        '''Returns an instance of the inheriting class that was packed into byte format.'''
        raise NotImplementedError

class GameStatus(IntEnum):
    Paused = 1
    Active = 2

class SharedGameState(ISendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Provides methods for sending and receiving SharedGameState objects via UDP sockets.
    '''

    def __init__(self, game_status=GameStatus.Paused):
        self.game_status = game_status

    '''
    Implementation of ISendable interface
    '''
    @staticmethod
    def from_bytes(bytepack):
        '''Decodes a a bytes object into a SharedGameState.'''
        receivedGameState = umsgpack.unpackb(bytepack)
        try:
            return SharedGameState(game_status=receivedGameState['game_status'])
        except KeyError:
            raise TypeError('Bytes could no be parsed into SharedGameState.')
    
    '''
    Overrides of object member functions
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_status == other.game_status
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)