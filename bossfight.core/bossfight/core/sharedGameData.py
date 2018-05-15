# -*- coding: utf-8 -*-

from enum import IntEnum
import umsgpack

class Sendable:
    '''
    Interface for objects that are supposed to be sendable as part of a server request or response.
    Inheriting classes must implement the static method *from_bytes(bytepack)* like this:
    `def from_bytes(bytepack): return super().from_bytes(subclass, bytepack)`
    Sendables can only have basic Python types as attributes and their constructor needs
    to be callable without passing any arguments.
    '''

    def to_bytes(self):
        '''
        Packs and return a small a binary representation of self.

        '''
        return umsgpack.packb(self.__dict__)

    @staticmethod
    def from_bytes(target_class: type, bytepack: bytes):
        '''
        Returns an instance of target_class that was packed into byte format.
        Should be implemented by subclasses by calling *Sendable.from_bytes(target_class, bytepack)*
        '''
        try:
            received_sendable = target_class()
            received_sendable.__dict__ = umsgpack.unpackb(bytepack)
            return received_sendable
        except KeyError:
            raise TypeError('Bytes could no be parsed into ' + target_class.__name__ + '.')

class GameStatus(IntEnum):
    '''
    Enum class with the values:
    - *Paused*
    - *Active*
    '''
    Paused = 1
    Active = 2

class SharedGameState(Sendable):
    '''
    Contains game state information that is required to be known both by the server and the client.
    Provides methods for sending and receiving *SharedGameState* objects via *GameService* and
    *GameServiceConnection*.
    '''

    def __init__(self, game_status=GameStatus.Paused):
        self.game_status = game_status

    '''
    Implementation of ISendable interface
    '''
    @staticmethod
    def from_bytes(bytepack: bytes):
        '''Decodes a a bytes object into a *SharedGameState*.'''
        return Sendable.from_bytes(SharedGameState, bytepack)

    '''
    Overrides of object member functions
    '''
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.game_status == other.game_status
        return False

    def __ne__(self, other):
        return not self.__eq__(other)
